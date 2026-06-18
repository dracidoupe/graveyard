from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib
import hmac
import logging

from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.db.models import F

from ddcz.models import (
    ScheduledEmail,
    BlacklistedEmail,
    EmailSubscriptionAuth,
    UserProfile,
    CreationEmailSubscription,
)
from ddcz.notifications import MAX_EMAIL_BATCH
from django.urls import reverse

logger = logging.getLogger(__name__)

EMAIL_UNSUB_HMAC_ALGORITHM = "sha3_512"

# Salt for signed tokens embedded in admin notification emails.
# Each token encodes the registration id and the intended action ("approve"/"reject").
REGISTRATION_REVIEW_SALT = "dragon.registration-review"
# Tokens are valid for this many seconds (30 days).
REGISTRATION_REVIEW_TOKEN_MAX_AGE = 30 * 24 * 60 * 60


def build_registration_review_url(reg_id, action):
    """Return an absolute URL for the admin registration-review confirmation page.

    action must be "approve" or "reject".
    """
    token = signing.dumps(
        {"id": reg_id, "action": action}, salt=REGISTRATION_REVIEW_SALT
    )
    return settings.EMAIL_LINKS_BASE_URI + reverse(
        "dragon:registration-review", kwargs={"token": token}
    )


def notify_admins_about_registration(reg):
    """Send a notification email to all staff users about a new registration request.

    Each admin receives an individual email (so their addresses aren't exposed to
    each other) containing signed Approve/Deny links for the review confirmation page.
    """
    recipients = list(
        UserProfile.objects.filter(user__is_staff=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )
    if not recipients:
        logger.warning(
            "New registration %s created but no staff users with an email found to notify",
            reg.id,
        )
        return

    approve_url = build_registration_review_url(reg.id, "approve")
    reject_url = build_registration_review_url(reg.id, "reject")
    subject = "Nová žádost o registraci na DraciDoupe.cz"
    body = (
        f"Ahoj,\n\n"
        f"je potřeba schválit novou registraci!\n\n"
        f"Přezdívka: {reg.nick}\n"
        f"E-mail: {reg.email}\n"
        f"Jméno: {reg.name_given} {reg.name_family}\n"
        f"Pohlaví: {reg.gender}    Věk: {reg.age}\n\n"
        f"Důvod / popis:\n{reg.description}\n\n"
        f"Schválit registraci: {approve_url}\n"
        f"Zamítnout registraci: {reject_url}\n\n"
        f"(Pro potvrzení akce je třeba přihlášení do správy.)\n\n"
        f"— DraciDoupe.cz"
    )
    # temporary hardcode
    recipients = ["almad@dracidoupe.cz"]
    for email in recipients:
        send_mail(subject, body, settings.DDCZ_TRANSACTION_EMAIL_FROM, [email])


def hash_email(email):
    hash_wip = hashlib.new(BlacklistedEmail.CIPHER_NAME)
    hash_wip.update(email.encode(BlacklistedEmail.CIPHER_CLEARTEXT_ENCODING))
    return hash_wip.hexdigest()


def get_unsubscribe_link(user_profile_id, email):
    try:
        token_secret = EmailSubscriptionAuth.objects.get(
            user_profile_id=user_profile_id
        ).token_secret
    except EmailSubscriptionAuth.DoesNotExist:
        unsub = EmailSubscriptionAuth(
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
    token_secret = EmailSubscriptionAuth.objects.get(
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
        EmailSubscriptionAuth.objects.filter(user_profile_id=profile.id).delete()

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
