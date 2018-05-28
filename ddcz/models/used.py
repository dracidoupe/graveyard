# This module contains models that are acutally used in the current state
# of the application
# It still represents a "transitional" state needed to cooperate with
# the old application; hence do not grin at missing ForeignKeys and similar
# "rooms for improvement" that can be done once the original application
# is strangled out of its existence

from django.db import models

from .magic import MisencodedCharField, MisencodedTextField


class News(models.Model):
    datum = models.DateTimeField()
    autor = MisencodedTextField()
    autmail = MisencodedTextField()
    text = MisencodedTextField()

    class Meta:
        managed = False
        db_table = 'aktuality'
        verbose_name = 'Aktuality'
        verbose_name_plural = "Aktuality"
        
    def __str__(self):
        return "{} dne {} v {}: {}".format(
            self.autor,
            self.datum.strftime("%d. %m. %Y"),
            self.datum.strftime("%X"),
            self.text[0:50]
        )

