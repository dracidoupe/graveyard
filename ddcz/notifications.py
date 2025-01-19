from datetime import timedelta
from enum import Enum
import logging
import json

from django.core import serializers
from django.utils import timezone

from ddcz.models import (
    NotificationEvent,
    ScheduledNotification,
    ScheduledEmail,
    UserProfile,
    CreationEmailSubscription,
)

logger = logging.getLogger(__name__)

MAX_NOTIFICATION_BATCH = 10000
MAX_EMAIL_BATCH = 500

ACTIVE_USER_INTERVAL = timedelta(days=365)
DECADE_USER_INTERVAL = timedelta(days=365 * 10)


class Audience(Enum):
    ACTIVE = "Aktivní uživatelé"
    LAST_DECADE = "Všichni z poslední dekády"
    # This should only be used for emergencies like password leaks
    EMERGENCY_EVERYONE = "Úplně všichni (JEN BEZPEČNOSTNÍ UPOZORNĚNÍ)"


class MailingSectionSlug(Enum):
    NEWS = "aktuality"


def schedule_notification(*, event, affected_object, extra_data):
    """
    Schedule notifying users about a given event.

    @returns right after scheduling the event. Notification delivery, retries and failures is handled separately
    """
    # TODO: Currently only resolves email sending. Later on, weekly letters, notification center in the news section
    # and others should be added
    # All other events triggering emails should also migrate to use notification center once API is figured out
    ScheduledNotification.objects.create(
        event=event.value,
        serialized_model=serializers.serialize("json", [affected_object]),
        extra_data=json.dumps(extra_data),
    )


def notify_scheduled():
    """
    Go through scheduled notifications and generate actual notifications from them.

    For email notifications, those are not scheduled directly but added to another queue instead. See `send_email_batch`
    """
    successful_notifications_id = []
    for notification in ScheduledNotification.objects.all()[0:MAX_NOTIFICATION_BATCH]:
        try:
            EVENT_DISPATCH_MAP[NotificationEvent(notification.event)](
                affected_object=list(
                    serializers.deserialize("json", notification.serialized_model)
                )[0].object,
                extra_data=json.loads(notification.extra_data),
            )
        except Exception as e:
            logger.warning(e, exc_info=True)
        else:
            successful_notifications_id.append(notification.id)

    ScheduledNotification.objects.filter(id__in=successful_notifications_id).delete()

    remaining = ScheduledNotification.objects.count()
    if remaining > 0:
        logger.warning(f"{remaining} notifications left")


def get_news_subscribers(audience):
    if audience == Audience.EMERGENCY_EVERYONE:
        raise NotImplementedError("Can't sent email to everyone yet")
    elif audience == Audience.ACTIVE:
        candidate_user_ids = UserProfile.objects.filter(
            last_login__gte=timezone.now() - ACTIVE_USER_INTERVAL
        ).values_list("id", flat=True)
    elif audience == Audience.LAST_DECADE:
        candidate_user_ids = UserProfile.objects.filter(
            last_login__gte=timezone.now() - DECADE_USER_INTERVAL
        ).values_list("id", flat=True)
    else:
        raise ValueError(f"Unknown audience {audience}")

    # From candidate users, select those who subscribed for News
    return list(
        CreationEmailSubscription.objects.filter(
            user_profile_id__in=candidate_user_ids,
            creative_page_slug=MailingSectionSlug.NEWS.value,
        ).values("user_email", "user_profile_id")
    )


def notify_news(affected_object, extra_data):
    audience = Audience(extra_data["audience"])

    subscribers = get_news_subscribers(audience)

    email_subject = "Aktualita serveru DraciDoupe.cz"
    email_text = f"""{affected_object.text}

    {extra_data["author_nick"]}
    """

    for subscriber in subscribers:
        ScheduledEmail.objects.create(
            recipient_email=subscriber["user_email"],
            user_profile_id=subscriber["user_profile_id"],
            email_subject=email_subject,
            email_text=email_text,
        )


EVENT_DISPATCH_MAP = {NotificationEvent.NEWS_ADDED: notify_news}
