# -*- coding: utf-8 -*-

from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField


class EditorArticle(models.Model):
    """Static editor article written by editors and maintained via admin"""

    title = models.CharField(max_length=40, verbose_name="Jméno")
    slug = models.CharField(max_length=40, unique=True)
    text = models.TextField()

    class Meta:
        verbose_name = "Redakční článek"
        verbose_name_plural = "Redakční články"


class News(models.Model):
    datum = models.DateTimeField()
    autor = MisencodedTextField()
    autmail = MisencodedTextField()
    text = MisencodedTextField()

    class Meta:
        db_table = "aktuality"
        verbose_name = "Aktuality"
        verbose_name_plural = "Aktuality"

    def __str__(self):
        return "{} dne {} v {}: {}".format(
            self.autor,
            self.datum.strftime("%d. %m. %Y"),
            self.datum.strftime("%X"),
            self.text[0:50],
        )
