# -*- coding: utf-8 -*-

from django.db import models


class EditorArticle(models.Model):
    """Static editor article written by editors and maintained via admin"""

    title = models.CharField(max_length=40, verbose_name="Jméno")
    slug = models.CharField(max_length=40, unique=True)
    text = models.TextField()

    class Meta:
        verbose_name = "Redakční článek"
        verbose_name_plural = "Redakční články"
