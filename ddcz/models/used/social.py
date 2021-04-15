from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField


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
    sekce = MisencodedCharField(max_length=20)
    jmeno = MisencodedCharField(max_length=30, blank=True, null=True)
    mail = MisencodedCharField(max_length=30, blank=True, null=True)
    telefon = MisencodedCharField(max_length=15, blank=True, null=True)
    mobil = MisencodedCharField(max_length=15, blank=True, null=True)
    okres = MisencodedCharField(max_length=20, blank=True, null=True)
    text = MisencodedTextField()
    datum = MisencodedCharField(max_length=12)

    class Meta:
        db_table = "inzerce"
        verbose_name = "Inzerce"
        verbose_name_plural = "Inzerce"
