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


class CommonArticles(models.Model):
    jmeno = MisencodedTextField()
    text = MisencodedTextField()
    autor = MisencodedCharField(max_length=25, blank=True, null=True)
    autmail = MisencodedCharField(max_length=30, blank=True, null=True)
    datum = models.DateTimeField()
    schvaleno = MisencodedCharField(max_length=1)
    zdroj = MisencodedTextField(blank=True, null=True)
    zdrojmail = MisencodedCharField(max_length=30, blank=True, null=True)
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)
    pochvez = MisencodedCharField(max_length=5)
    precteno = models.IntegerField()
    tisknuto = models.IntegerField()
    skupina = MisencodedCharField(max_length=30, blank=True, null=True)
    anotace = MisencodedTextField(blank=True, null=True)
    rubrika = MisencodedCharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'prispevky_dlouhe'
        verbose_name = 'Běžné příspěvky'
        verbose_name_plural = 'Běžné příspěvky'

    def __str__(self):
        return "{} od {}".format(
            self.jmeno,
            self.autor,
        )
