from django.db import models
from ..magic import MisencodedCharField, MisencodedTextField


from .creations import *
from .discussion import *
from .info import *
from .social import *
from .tavern import *
from .users import *


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
