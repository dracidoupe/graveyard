from datetime import timedelta
from enum import Enum
import logging
import json

from django.conf import settings
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import F
from django.utils import timezone

from ddcz.models import (
    NotificationEvent,
    ScheduledNotification,
    ScheduledEmail,
    UserProfile,
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


def schedule_notification(*, event, affected_object, extra_data):
    """
    Schedule notifying users about a given event.

    @returns right after scheduling the event. Notification delivery, retries and failures is handled separately
    """
    # TODO: Currently only resolves email sending. Later on, weekly letters, notification center in the news section
    # and others should be added
    # All other events triggering emails should also migrate to use notification center once API is figured out
    ScheduledNotification.objects.create(
        event=event,
        serialized_model=serializers.serialize("json", [affected_object]),
        extra_data=json.dumps(extra_data),
    )


def send_email_batch():
    sent_ids = []
    failures = []
    for scheduled_email in ScheduledEmail.objects.all()[0:MAX_EMAIL_BATCH]:
        try:
            send_mail(
                scheduled_email.email_subject,
                scheduled_email.email_text,
                settings.DDCZ_TRANSACTION_EMAIL_FROM,
                [scheduled_email.recipient_email],
            )
        except Exception as e:
            logger.warning(f"Sending email {scheduled_email.pk} failed: ", e)
            failures.append(scheduled_email.id)
        else:
            sent_ids.append(scheduled_email.id)

    ScheduledEmail.objects.filter(id__in=sent_ids).delete()
    ScheduledEmail.objects.filter(id__in=failures).update(failures=F("failures") + 1)


def notify_scheduled():
    """
    Go through scheduled notifications and generate actual notifications from them.

    For email notifications, those are not scheduled directly but added to another queue instead. See `send_email_batch`
    """
    successful_notifications_id = []
    for notification in ScheduledNotification.objects.all()[0:MAX_NOTIFICATION_BATCH]:
        try:
            EVENT_DISPATCH_MAP[NotificationEvent(notification.event)](
                affected_object=serializers.deserialize(
                    "json", notification.serialized_model
                )[0],
                extra_data=json.loads(notification.extra_data),
            )
        except Exception as e:
            logger.warning("Notification failed: ", e)
        else:
            successful_notifications_id.append(notification.id)

    ScheduledNotification.objects.filter(id__in=successful_notifications_id).delete()

    remaining = ScheduledNotification.objects.count()
    if remaining > 0:
        logger.warning(f"{remaining} notifications left")


def get_emails_for_news(audience):
    if audience == Audience.EMERGENCY_EVERYONE:
        raise NotImplementedError("Can't sent email to everyone yet")
    elif audience == Audience.ACTIVE:
        candidate_users = UserProfile.objects.filter(
            last_login__gte=timezone.now() - ACTIVE_USER_INTERVAL
        )
    elif audience == Audience.LAST_DECADE:
        candidate_users = UserProfile.objects.filter(
            last_login__gte=timezone.now() - DECADE_USER_INTERVAL
        )
    else:
        raise ValueError(f"Unknown audience {audience}")

    # From candidate users, select those who subscribed for News

    # and return their emails
    return []


def notify_news(affected_object, extra_data):
    audience = Audience(extra_data["audience"])

    emails = get_emails_for_news(audience)

    email_subject = "Aktualita serveru DraciDoupe.cz"
    email_text = f"""{affected_object.text}

    — {extra_data['author_nick']}
    """

    for email in emails:
        ScheduledEmail.objects.create(
            recipient_email=email, email_subject=email_subject, email_text=email_text
        )


EVENT_DISPATCH_MAP = {NotificationEvent.NEWS_ADDED: notify_news}
