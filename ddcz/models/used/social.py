from datetime import date
from time import strptime

from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField

MARKET_SECTION_CHOICES = (
    ("nabizim", "Nabízím"),
    ("shanim", "Sháním"),
    ("vymenim", "Vyměním"),
    ("daruji", "Daruji"),
)


class Dating(models.Model):
    jmeno = MisencodedCharField(max_length=40, blank=True, null=True)
    email = MisencodedCharField(max_length=40, blank=True, null=True)
    telefon = MisencodedCharField(max_length=20, blank=True, null=True)
    mobil = MisencodedCharField(max_length=20, blank=True, null=True)
    vek = models.IntegerField(blank=True, null=True)
    okres = MisencodedCharField(max_length=40, blank=True, null=True)
    doba = MisencodedCharField(max_length=20, blank=True, null=True)
    datum = models.DateTimeField(blank=True, null=True)
    text = MisencodedTextField(blank=True, null=True)
    sekce = MisencodedCharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "seznamka"
        verbose_name = "Seznamka"
        verbose_name_plural = "Seznamky"


class Market(models.Model):
    sekce = MisencodedCharField(max_length=20, choices=MARKET_SECTION_CHOICES)
    jmeno = MisencodedCharField(max_length=30, blank=True, null=True)
    mail = MisencodedCharField(max_length=30, blank=True, null=True)
    telefon = MisencodedCharField(max_length=15, blank=True, null=True)
    mobil = MisencodedCharField(max_length=15, blank=True, null=True)
    okres = MisencodedCharField(max_length=20, blank=True, null=True)
    text = MisencodedTextField()
    # WARNING WARNING WARNING, not a Date, but a varchar instead!
    # Old version stores in the Czech format: dd. mm. YYYY (where d/m is without leading 0)
    # See https://github.com/dracidoupe/graveyard/issues/195
    datum = MisencodedCharField(max_length=12)

    @property
    def date(self):
        # Windows workaround as `%-d` is platform-specific
        try:
            return date(*(strptime(self.datum, "%-d. %-m. %Y")[0:3]))
        except ValueError:
            return date(*(strptime(self.datum, "%d. %m. %Y")[0:3]))

    class Meta:
        db_table = "inzerce"
        verbose_name = "Inzerce"
        verbose_name_plural = "Inzerce"
