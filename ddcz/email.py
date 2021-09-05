from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib
import hmac
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F

from ddcz.models import (
    ScheduledEmail,
    BlacklistedEmail,
    UnsubscribedEmail,
    UserProfile,
    CreationEmailSubscription,
)
from ddcz.notifications import MAX_EMAIL_BATCH, logger
from django.urls import reverse

logger = logging.getLogger(__name__)

EMAIL_UNSUB_HMAC_ALGORITHM = "sha3_512"


def hash_email(email):
    hash_wip = hashlib.new(BlacklistedEmail.CIPHER_NAME)
    hash_wip.update(email.encode(BlacklistedEmail.CIPHER_CLEARTEXT_ENCODING))
    return hash_wip.hexdigest()


def get_unsubscribe_link(user_profile_id, email):
    try:
        token_secret = UnsubscribedEmail.objects.get(
            user_profile_id=user_profile_id
        ).token_secret
    except UnsubscribedEmail.DoesNotExist:
        unsub = UnsubscribedEmail(
            # The query is to double-check we are using valid profile PK and not an arbitrary number
            user_profile_id=UserProfile.objects.get(id=user_profile_id).id
        )
        token_secret = unsub.generate_token()
        unsub.save()

    token_hash = hmac.new(
        key=token_secret.encode(settings.CRYPTO_TEXT_ENCODING),
        msg=email.encode(settings.CRYPTO_TEXT_ENCODING),
        digestmod=EMAIL_UNSUB_HMAC_ALGORITHM,
    )
    token = token_hash.hexdigest()

    return settings.EMAIL_LINKS_BASE_URI + reverse(
        "ddcz:email-antispam",
        kwargs={
            "email_base64": urlsafe_b64encode(
                email.encode(settings.CRYPTO_TEXT_ENCODING)
            ).decode("ascii"),
            "unsub_token": token,
        },
    )


def validate_unsubscribe_token(email_base64, unsub_token):
    email = urlsafe_b64decode(email_base64.encode("ascii")).decode(
        settings.CRYPTO_TEXT_ENCODING
    )
    profile = UserProfile.objects.only("id").get(email=email)
    token_secret = UnsubscribedEmail.objects.get(
        user_profile_id=profile.id
    ).token_secret

    token_hash = hmac.new(
        key=token_secret.encode(settings.CRYPTO_TEXT_ENCODING),
        msg=email.encode(settings.CRYPTO_TEXT_ENCODING),
        digestmod=EMAIL_UNSUB_HMAC_ALGORITHM,
    )
    expected_token = token_hash.hexdigest()

    return hmac.compare_digest(expected_token, unsub_token)


def blacklist_email(email_base64):
    logger.info(f"Blacklisting email {email_base64}")

    email = urlsafe_b64decode(
        email_base64.encode(settings.CRYPTO_TEXT_ENCODING)
    ).decode(settings.CRYPTO_TEXT_ENCODING)
    # Put on priority blacklist
    BlacklistedEmail.objects.create(email_hash=hash_email(email))

    try:
        profile = UserProfile.objects.only("id").get(email=email)
    except UserProfile.DoesNotExist:
        profile = None

    CreationEmailSubscription.objects.filter(user_email=email).delete()
    if profile:
        CreationEmailSubscription.objects.filter(user_profile_id=profile.id).delete()
        UnsubscribedEmail.objects.filter(user_profile_id=profile.id).delete()

    # TODO: Do the same for diskuze_maillist


def send_email_batch():
    sent_ids = []
    failures = []

    blacklisted_emails = list(
        BlacklistedEmail.objects.all().values_list("email_hash", flat=True)
    )

    # Let's say give in-memory caching 25MB budget. AVG address ~30chars ~= 30bytes = 873813 emails
    if len(blacklisted_emails) > 873813:
        logger.warning(
            "Too many blacklisted emails. Consider not loading them in memory and do a database lookup instead"
        )

    for scheduled_email in ScheduledEmail.objects.all()[0:MAX_EMAIL_BATCH]:
        email_hash = hash_email(scheduled_email.recipient_email)

        if email_hash in blacklisted_emails:
            logger.error(
                f"Attempted to send an email to a blacklisted email (scheduled email ID {scheduled_email.pk}, hash {email_hash}). Investigate!"
            )
            failures.append(scheduled_email.id)
        else:
            unsub_link = get_unsubscribe_link(
                user_profile_id=scheduled_email.user_profile_id,
                email=scheduled_email.recipient_email,
            )
            text = (
                scheduled_email.email_text
                + f"""

            Upravit zasílání e-mailů můžete v nastavení. Pokud již nikdy nechcete na tento e-mail dostávat žádné zprávy, navštivte tento odkaz: {unsub_link}
            """
            )

            try:
                send_mail(
                    scheduled_email.email_subject,
                    text,
                    settings.DDCZ_TRANSACTION_EMAIL_FROM,
                    [scheduled_email.recipient_email],
                )
            except Exception as e:
                logger.warning(f"Sending email {scheduled_email.pk} failed: ", e)
                failures.append(scheduled_email.id)
            else:
                sent_ids.append(scheduled_email.id)

    ScheduledEmail.objects.filter(id__in=sent_ids).delete()
    ScheduledEmail.objects.filter(id__in=failures).update(
        sending_failures=F("sending_failures") + 1
    )
