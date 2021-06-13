from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField


class ReputationLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_zaznamu")
    donor = models.CharField(max_length=30, db_column="dal")
    donee = models.CharField(max_length=30, db_column="prijal")
    action = models.CharField(max_length=3, db_column="akce")
    discussion = models.CharField(
        max_length=1, blank=True, null=True, db_column="v_diskuzi"
    )
    post = models.PositiveIntegerField(blank=True, null=True, db_column="id_prispevku")
    date = models.IntegerField()

    class Meta:
        db_table = "reputace_log"


class ReputationAdditional(models.Model):
    donee = models.CharField(max_length=25, db_column="prijal_nick")
    reason = models.CharField(max_length=200, db_column="duvod_udeleni")
    amount = models.IntegerField(db_column="hodnota")

    class Meta:
        db_table = "reputace_special"
