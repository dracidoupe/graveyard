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
    name = MisencodedCharField(
        max_length=40, blank=True, null=True, db_column="jmeno", verbose_name="Jméno"
    )
    email = MisencodedCharField(max_length=40, blank=True, null=True)
    phone = MisencodedCharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="telefon",
        verbose_name="Telefon",
    )
    mobile = MisencodedCharField(
        max_length=20, blank=True, null=True, db_column="mobil", verbose_name="Mobil"
    )
    age = models.IntegerField(
        blank=True, null=True, db_column="vek", verbose_name="Věk"
    )
    area = MisencodedCharField(
        max_length=40, blank=True, null=True, db_column="okres", verbose_name="Okres"
    )
    experience = MisencodedCharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="doba",
        verbose_name="Doba hraní DrD",
    )
    published = models.DateTimeField(
        blank=True, null=True, db_column="datum", verbose_name="Datum"
    )
    text = MisencodedTextField(blank=True, null=True, db_column="text")
    group = MisencodedCharField(
        max_length=20, blank=True, null=True, db_column="sekce", verbose_name="Sekce"
    )

    class Meta:
        db_table = "seznamka"
        verbose_name = "Seznamka"
        verbose_name_plural = "Seznamky"

    def __str__(self):
        return f"{self.name} ve skupině {self.group}"


class Market(models.Model):
    group = MisencodedCharField(
        max_length=20,
        choices=MARKET_SECTION_CHOICES,
        db_column="sekce",
        verbose_name="Sekce",
    )
    name = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="jmeno", verbose_name="Jméno"
    )
    mail = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="mail", verbose_name="E-mail"
    )
    phone = MisencodedCharField(
        max_length=15,
        blank=True,
        null=True,
        db_column="telefon",
        verbose_name="Telefon",
    )
    mobile = MisencodedCharField(
        max_length=15, blank=True, null=True, db_column="mobil", verbose_name="Mobil"
    )
    area = MisencodedCharField(
        max_length=20, blank=True, null=True, db_column="okres", verbose_name="Okres"
    )
    text = MisencodedTextField()
    # WARNING WARNING WARNING, not a Date, but a varchar instead!
    # Old version stores in the Czech format: dd. mm. YYYY (where d/m is without leading 0)
    # See https://github.com/dracidoupe/graveyard/issues/195
    published_varchar = MisencodedCharField(
        max_length=12, db_column="datum", verbose_name="Přidáno"
    )

    created = models.DateTimeField(blank=True, null=True, verbose_name="Přidáno")

    @property
    def published(self):
        # Windows workaround as `%-d` is platform-specific
        try:
            return date(*(strptime(self.published_varchar, "%-d. %-m. %Y")[0:3]))
        except ValueError:
            return date(*(strptime(self.published_varchar, "%d. %m. %Y")[0:3]))

    class Meta:
        db_table = "inzerce"
        verbose_name = "Inzerce"
        verbose_name_plural = "Inzerce"
