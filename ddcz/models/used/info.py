# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse

from ..magic import MisencodedTextField, MisencodedCharField


class EditorArticle(models.Model):
    """Static editor article written by editors and maintained via admin"""

    title = MisencodedCharField(max_length=40, verbose_name="Jméno")
    slug = models.CharField(max_length=40, unique=True)
    text = MisencodedTextField()

    class Meta:
        verbose_name = "Redakční článek"
        verbose_name_plural = "Redakční články"

    def __str__(self):
        return self.title


class News(models.Model):
    date = models.DateTimeField(db_column="datum")
    author = MisencodedTextField(db_column="autor")
    author_mail = MisencodedTextField(db_column="autmail")
    text = MisencodedTextField(db_column="text")

    class Meta:
        db_table = "aktuality"
        verbose_name = "Aktuality"
        verbose_name_plural = "Aktuality"

    def __str__(self):
        return "{} dne {} v {}: {}".format(
            self.author,
            self.date.strftime("%d. %m. %Y"),
            self.date.strftime("%X"),
            self.text[0:50],
        )

    def get_absolute_url(self):
        return reverse("ddcz:news")
