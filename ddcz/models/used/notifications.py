# -*- coding: utf-8 -*-
from enum import Enum

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
