# -*- coding: utf-8 -*-
from base64 import urlsafe_b64decode
from enum import Enum
from secrets import token_urlsafe

from django.db import models

# I'd prefer this to be in ddcz.notifications, but we can't as it's used in charfield choices
# and I want to avoid circular imports


class NotificationEvent(Enum):
    NEWS_ADDED = "Nová aktualita"


class ScheduledNotification(models.Model):
    event = models.CharField(
        choices=((i.name, i.value) for i in NotificationEvent), max_length=255
    )
    serialized_model = models.TextField()
    extra_data = models.TextField()
    scheduled_at = models.DateTimeField(auto_now_add=True)


class ScheduledEmail(models.Model):
    recipient_email = models.CharField(max_length=150)
    email_subject = models.CharField(max_length=255)
    email_text = models.TextField()
    sending_failures = models.IntegerField(default=0)
    scheduled_at = models.DateTimeField(auto_now_add=True)
    # TODO: Migration to foreign key
    user_profile_id = models.IntegerField()


class CreationEmailSubscription(models.Model):
    user_profile_id = models.IntegerField(db_column="id_uz")
    creative_page_slug = models.CharField(max_length=20, db_column="rubrika")
    user_email = models.CharField(max_length=40, db_column="email_uz")
    # MIME can be ignored for now (I think it was meant to be used to select between HTML
    # and plain, but was never used and hence it's always set to "p"
    mime = models.CharField(
        db_column="MIME", max_length=1
    )  # Field name made lowercase.

    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "uzivatele_maillist"
        unique_together = (("user_profile_id", "creative_page_slug"),)


class BlacklistedEmail(models.Model):
    # SHA512 is used. In case of extending, we cannot rehash anyway, so we'll add
    # additional field with cipher type
    # If the purpose would be to only validate links, it would be better to use password-like
    # strong crypt (blake/scrypt/...), but here we need to do a global lookup against the whole
    # table, not per-item validation. sha512 seems like a good tradeoff for lookup ability
    # vs. how hard it would be to get the mails in case of the leak
    # The database is not large enough to be worth it given the current state of the black market
    CIPHER_NAME = "sha3_512"
    CIPHER_CLEARTEXT_ENCODING = "utf8"
    email_hash = models.CharField(max_length=255, primary_key=True)


class EmailSubscriptionAuth(models.Model):
    # TODO: Foreign Key is only usable between InnoDB tables
    # Migrate after all tables are migrated, see <https://github.com/dracidoupe/graveyard/issues/109>
    # user_profile = models.OneToOneField(
    #     "UserProfile", primary_key=True, on_delete=models.CASCADE
    # )
    user_profile_id = models.IntegerField(primary_key=True)
    token_secret = models.CharField(max_length=255)

    def generate_token(self):
        self.token_secret = token_urlsafe()
        return self.token_secret

    def save(self, *args, **kwargs):
        if not self.token_secret:
            self.generate_token()
        super().save(*args, **kwargs)
