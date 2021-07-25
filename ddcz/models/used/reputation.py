from django.db import models

from ..magic import MisencodedCharField


class ReputationLog(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_zaznamu")
    donor = MisencodedCharField(max_length=30, db_column="dal")
    donee = MisencodedCharField(max_length=30, db_column="prijal")
    action = MisencodedCharField(max_length=3, db_column="akce")
    # Note: this is a ChoiceField: enum('a','n','z','s','f')
    # a = article discussion
    # n = Tavern
    # f = Phorum
    # z and s needs research, candidates are s for special and z for Golden Dragon Award
    discussion = MisencodedCharField(
        max_length=1, blank=True, null=True, db_column="v_diskusi"
    )
    post = models.PositiveIntegerField(blank=True, null=True, db_column="id_prispevku")
    date = models.IntegerField()

    class Meta:
        db_table = "reputace_log"


class ReputationAdditional(models.Model):
    donee = MisencodedCharField(max_length=25, db_column="prijal_nick")
    reason = MisencodedCharField(max_length=200, db_column="duvod_udeleni")
    amount = models.IntegerField(db_column="hodnota")

    class Meta:
        db_table = "reputace_special"
