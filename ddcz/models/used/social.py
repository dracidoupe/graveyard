from django.db import models
from django.urls import reverse
from ..magic import MisencodedCharField, MisencodedTextField
from ..used.users import UserProfile

MARKET_SECTION_CHOICES = (
    ("nabizim", "Nabízím"),
    ("shanim", "Sháním"),
    ("vymenim", "Vyměním"),
    ("daruji", "Daruji"),
)

DATING_SECTION_CHOICES = (
    ("hledam_hrace", "Hledám hráče"),
    ("hledam_druzinu", "Hledám družinu"),
    ("hledam_pj", "Hledám PJ"),
    ("nabizim_druzinu", "Nabízím družinu"),
    ("nabizim_pj", "Nabízím se jako PJ"),
)


class Dating(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    name = MisencodedCharField(
        max_length=40, db_column="jmeno", verbose_name="Jméno", default="Anonym"
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
        max_length=40, blank=True, null=True, db_column="okres", verbose_name="Kraj"
    )
    experience = MisencodedCharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="doba",
        verbose_name="Doba hraní DrD",
    )
    published = models.DateTimeField(
        blank=True,
        null=True,
        db_column="datum",
        verbose_name="Datum",
        auto_now_add=True,
    )
    text = MisencodedTextField(db_column="text")
    group = MisencodedCharField(
        max_length=20,
        choices=DATING_SECTION_CHOICES,
        db_column="sekce",
        verbose_name="Sekce",
    )

    class Meta:
        db_table = "seznamka"
        verbose_name = "Seznamka"
        verbose_name_plural = "Seznamky"

    def __str__(self):
        return f"{self.name} ve skupině {self.group}"

    def get_absolute_url(self):
        return reverse("ddcz:dating")


class Market(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    group = MisencodedCharField(
        max_length=20,
        choices=MARKET_SECTION_CHOICES,
        db_column="sekce",
        verbose_name="Sekce",
    )
    name = MisencodedCharField(
        max_length=100, blank=True, null=True, db_column="jmeno", verbose_name="Jméno"
    )
    mail = MisencodedCharField(
        max_length=50, blank=True, null=True, db_column="mail", verbose_name="E-mail"
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
    # Originally okres, but those stopped being used meanwhile, and kraj makes more sense
    # than underlying counties or whatever
    area = MisencodedCharField(
        max_length=20, blank=True, null=True, db_column="okres", verbose_name="Kraj"
    )
    text = MisencodedTextField()
    created = models.DateTimeField(verbose_name="Přidáno", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group}) z {self.published}"

    @property
    def published(self):
        return self.created

    class Meta:
        db_table = "inzerce"
        verbose_name = "Inzerce"
        verbose_name_plural = "Inzerce"
