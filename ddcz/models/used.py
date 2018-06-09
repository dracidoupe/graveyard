# This module contains models that are acutally used in the current state
# of the application
# It still represents a "transitional" state needed to cooperate with
# the old application; hence do not grin at missing ForeignKeys and similar
# "rooms for improvement" that can be done once the original application
# is strangled out of its existence

import re
from unicodedata import normalize, combining

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from .magic import MisencodedCharField, MisencodedTextField
from ..commonarticles import COMMON_ARTICLES_CREATIVE_PAGES

APPROVAL_CHOICES = (
    ('a', 'Schváleno'),
    ('n', 'Neschváleno'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    jmeno_uzivatele = MisencodedCharField(max_length=20)
    nick_uzivatele = MisencodedCharField(unique=True, max_length=25)
    prijmeni_uzivatele = MisencodedCharField(max_length=20)
    psw_uzivatele = MisencodedCharField(max_length=40)
    email_uzivatele = MisencodedCharField(max_length=50)
    pohlavi_uzivatele = MisencodedCharField(max_length=4, blank=True, null=True)
    vek_uzivatele = models.IntegerField(default=0)
    kraj_uzivatele = MisencodedCharField(max_length=20)
    chat_barva = MisencodedCharField(max_length=6)
    chat_pismo = models.IntegerField(default=12)
    chat_reload = models.IntegerField(default=15)
    chat_zprav = models.IntegerField(default=20)
    chat_filtr = MisencodedCharField(max_length=255, blank=True, null=True)
    chat_filtr_zobrazit = models.IntegerField(default=0)
    pospristup = models.DateTimeField(auto_now_add=True)
    level = MisencodedCharField(max_length=1)
    icq_uzivatele = models.IntegerField(default=0)
    vypsat_udaje = MisencodedCharField(max_length=15)
    ikonka_uzivatele = MisencodedCharField(max_length=25, blank=True, null=True)
    popis_uzivatele = MisencodedCharField(max_length=255, blank=True, null=True)
    nova_posta = models.IntegerField(default=0)
    skin = MisencodedCharField(max_length=10)
    reputace = models.IntegerField(default=0)
    reputace_rozdel = models.PositiveIntegerField(default=0)
    status = MisencodedCharField(max_length=1)
    reg_schval_datum = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    indexhodnotitele = models.DecimalField(max_digits=4, decimal_places=2, default=-99.99)
    reload = MisencodedCharField(max_length=1)
    max_level = models.IntegerField(blank=True, null=True)
    api_key = MisencodedCharField(unique=True, max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'uzivatele'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Note that unlike the normal model, we are creating the User lazily
    # (instead of UserProfile as usual). Hence, on creation, UserProfile is assumed
    # to exist (and needs to be updated with proper relation manually), whereas
    # afterwards profiles can be updated as usual
    if created:
        # YOU are responsible for properly linking User and UserProfile
        # outside of signal handling!
        # ALWAYS use .users.create_user
        pass
    else:
        instance.profile.save()


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
    schvaleno = MisencodedCharField(max_length=1, choices=APPROVAL_CHOICES)
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
        return "{}: {} od {}".format(
            # COMMON_ARTICLES_CREATIVE_PAGES[self.rubrika]['name'],
            self.rubrika,
            self.jmeno,
            self.autor,
        )

    def get_slug(self):
        # slug = normalize('NKFD', self.jmeno)
        slug = normalize('NFD', self.jmeno)
        slug = ''.join([ch for ch in slug if not combining(ch)]).lower()
        slug = re.sub("[^a-z0-9]+", "-", slug)
        slug = re.sub("^([^a-z0-9])+", "", slug)
        slug = re.sub("([^a-z0-9]+)$", "", slug)
        return slug


class Dating(models.Model):
    jmeno = MisencodedCharField(max_length=40, blank=True, null=True)
    email = MisencodedCharField(max_length=40, blank=True, null=True)
    telefon = MisencodedCharField(max_length=20, blank=True, null=True)
    mobil = MisencodedCharField(max_length=20, blank=True, null=True)
    vek = models.IntegerField(blank=True, null=True)
    okres = MisencodedCharField(max_length=40, blank=True, null=True)
    doba = MisencodedCharField(max_length=20, blank=True, null=True)
    datum = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    sekce = MisencodedCharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'seznamka'
        verbose_name = 'Seznamka'
        verbose_name_plural = 'Seznamky'
