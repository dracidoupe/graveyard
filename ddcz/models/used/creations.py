# This module contains models that are acutally used in the current state
# of the application
# It still represents a "transitional" state needed to cooperate with
# the old application; hence do not grin at missing ForeignKeys and similar
# "rooms for improvement" that can be done once the original application
# is strangled out of its existence

import re
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from ...text import create_slug
from ..magic import MisencodedCharField, MisencodedTextField, MisencodedIntegerField
from .users import UserProfile

APPROVAL_CHOICES = (
    ('a', 'Schváleno'),
    ('n', 'Neschváleno'),
)

EMPTY_SLUG_PLACEHOLDER = 'dilo'

###
# Introduce an umbrella model for all Creations
###

class CreativePage(models.Model):
    """ I represent a Creative Page as a first-item concept to help with foreign keys, definitions etc. """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    model_class = models.CharField(max_length=50)
    # editors = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Rubrika'
        verbose_name_plural = 'Rubriky'

    def __str__(self):
        return "Rubrika {}".format(
            self.name,
        )


class CreativePageSection(models.Model):
    """ Section within a Creative Page """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

class CreativePageConcept(models.Model):
    page = models.OneToOneField(CreativePage, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = 'Koncept rubriky'
        verbose_name_plural = 'Koncepty rubriky'

    def __str__(self):
        return "Koncept rubriky {}".format(
            self.page.name,
        )

class Creation(models.Model):
    """
    Encapsulates common fields and actions for all creations. Please note:

        * This is introduced as a new concept in the rewrite, hence
            backward-compatible handling of all relations is needed
        * It may be tempting to add "popis" or "anotace" to the model, but
            note that (Photo)Gallery is part of this as well
        * Authors are _not_ handled using ForeignKeys -- this is to be introduced later
        * `pochvez` (aka rating) CAN'T be recomputed from CreationVotes since votes are not created equal:
            - Editor's vote is counted as three votes
            - The Head of a Gold Dragon Awards flatly marks winners as having six stars

            Neither of those is tracked in database very well and such information is lost.
            Be careful, don't lose aggregates!
    """
    jmeno = MisencodedTextField()
    autor = MisencodedCharField(max_length=50, blank=True, null=True)
    autmail = MisencodedCharField(max_length=50, blank=True, null=True)
    schvaleno = MisencodedCharField(max_length=1, choices=APPROVAL_CHOICES)
    zdroj = MisencodedTextField(blank=True, null=True)
    zdrojmail = MisencodedTextField(blank=True, null=True)
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)
    pochvez = MisencodedIntegerField(max_length=5)
    precteno = models.IntegerField(default=0)
    tisknuto = models.IntegerField(default=0)
    datum = models.DateTimeField(auto_now_add=True)

    # section = models.ForeignKey(CreativePageSection, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

    def get_author_profile(self):
        try:
            return UserProfile.objects.get(nick_uzivatele=self.autor)
        except UserProfile.DoesNotExist:
            return

    author_profile = property(get_author_profile)


    def get_slug(self):
        slug = create_slug(self.jmeno)
        return slug or EMPTY_SLUG_PLACEHOLDER

    def __str__(self):
        return "{} od {}".format(
            self.jmeno,
            self.autor
        )


###
# Handle all models that should work with all creations.
# Do note that for backward compatibility, all relations to creations
# has to be NULLable and that (lazy) migration is needed in order to fix
# this model
###


class CreationVotes(models.Model):
    # creation = models.OneToMany(Creation) -- to be introduced later
    #TODO: Would conversion to ForeignKey work..and would it work to User?
    id_uz = models.IntegerField(primary_key=True)
    id_cizi = models.IntegerField()
    rubrika = MisencodedCharField(max_length=20)
    pochvez = models.IntegerField()
    time = models.IntegerField()
    opraveno = MisencodedCharField(max_length=1)

    class Meta:
        db_table = 'hlasovani_prispevky'
        unique_together = (('id_uz', 'id_cizi', 'rubrika'),)


###
# Particular models for all creations follow
###

class CommonArticle(Creation):
    text = MisencodedTextField()
    skupina = MisencodedCharField(max_length=30, blank=True, null=True)
    anotace = MisencodedTextField(blank=True, null=True)
    rubrika = MisencodedCharField(max_length=30)

    class Meta:
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


###
# First, all "common" articles, just with extra fields
###

class Monster(Creation):
    zvt = MisencodedTextField()
    uc = MisencodedTextField()
    oc = MisencodedTextField()
    odl = MisencodedCharField(max_length=3)
    inteligence = MisencodedCharField(max_length=50, blank=True, null=True)
    vel = MisencodedCharField(max_length=20)
    zran = MisencodedTextField(blank=True, null=True)
    poh = MisencodedTextField(blank=True, null=True)
    pres = MisencodedTextField(blank=True, null=True)
    pokl = MisencodedTextField(blank=True, null=True)
    zkus = MisencodedCharField(max_length=50)
    popis = MisencodedTextField()
    skupina = MisencodedTextField()
    bojovnost = MisencodedCharField(max_length=50, blank=True, null=True)
    sm = MisencodedCharField(db_column='SM', max_length=50)  # Field name made lowercase.

    class Meta:
        db_table = 'bestiar'
        verbose_name = 'Nestvůra'
        verbose_name_plural = 'Bestiář'

    def __str__(self):
        return "{} od {}".format(
            self.jmeno,
            self.autor,
        )


###
# Creations that handle uploaded content
###


class GalleryPicture(Creation):
    """
    In the g'old days, picture uploads has to be done manually.

    Hence, this is a compatibility model to handle both old version
    (path stored in `cesta`) as well as new version 
    """
    cesta = MisencodedTextField()
    cestathumb = MisencodedTextField()

    class Meta:
        db_table = 'galerie'


    def get_thumbnail_url(self):
        return urljoin(
            settings.GALLERY_MEDIA_ROOT_URL,
            self.cestathumb
        )

    def get_picture_url(self):
        return urljoin(
            settings.GALLERY_MEDIA_ROOT_URL,
            self.cesta
        )
        

class Photo(Creation):
    """ See GalleryPicture; just part of different Creation Page """
    cesta = MisencodedTextField()
    cestathumb = MisencodedTextField()

    class Meta:
        db_table = 'fotogalerie'

    def get_thumbnail_url(self):
        return urljoin(
            settings.PHOTOGALLERY_MEDIA_ROOT_URL,
            self.cestathumb
        )

    def get_picture_url(self):
        return urljoin(
            settings.PHOTOGALLERY_MEDIA_ROOT_URL,
            self.cesta
        )


class Skill(Creation):
    vlastnost = MisencodedTextField()
    obtiznost = MisencodedTextField()
    overovani = MisencodedTextField()
    totuspech = MisencodedTextField()
    uspech = MisencodedTextField()
    neuspech = MisencodedTextField()
    fatneuspech = MisencodedTextField()
    popis = MisencodedTextField()
    skupina = MisencodedCharField(max_length=30)
    # TODO: No idea what this is used for, potentially drop
    hlasoval = MisencodedTextField(blank=True, null=True)

    class Meta:
        db_table = 'dovednosti'

class AlchemistTool(Creation):
    mag = models.IntegerField(blank=True, null=True)
    suroviny = models.SmallIntegerField(blank=True, null=True)
    zaklad = MisencodedCharField(max_length=150, blank=True, null=True)
    nalezeni = MisencodedCharField(max_length=150, blank=True, null=True)
    trvani = MisencodedCharField(max_length=30, blank=True, null=True)
    vyroba = MisencodedCharField(max_length=30, blank=True, null=True)
    nebezpecnost = MisencodedCharField(max_length=30, blank=True, null=True)
    sila = MisencodedCharField(max_length=30, blank=True, null=True)
    bcz = MisencodedCharField(max_length=30, blank=True, null=True)
    denmag = models.IntegerField(blank=True, null=True)
    dosah_ucinku = MisencodedCharField(max_length=20, blank=True, null=True)
    uroven_vyrobce = MisencodedCharField(max_length=10)
    sfera = MisencodedCharField(max_length=20)
    popis = MisencodedTextField()
    skupina = MisencodedCharField(max_length=30)

    class Meta:
        db_table = 'alchpredmety'

    def __str__(self):
        return "{} od {}".format(
            self.jmeno,
            self.autor,
        )


class Link(models.Model):
    nazev = MisencodedTextField()
    adresa = MisencodedTextField()
    popis = MisencodedTextField()
    pochvez = MisencodedCharField(max_length=1)
    schvaleno = MisencodedCharField(max_length=1, choices=APPROVAL_CHOICES)
    datum = models.DateTimeField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'linky'

    def __str__(self):
        return "{} {}".format(
            self.nazev,
            self.adresa
        )


class RangerSpell(Creation):
    mag = models.SmallIntegerField()
    magpop = MisencodedTextField()
    dosah = models.SmallIntegerField(blank=True, null=True)
    dosahpop = MisencodedTextField(blank=True, null=True)
    rozsah = models.SmallIntegerField(blank=True, null=True)
    rozsahpop = MisencodedTextField(blank=True, null=True)
    vyvolani = models.SmallIntegerField(blank=True, null=True)
    vyvolanipop = MisencodedTextField(blank=True, null=True)
    druh = MisencodedTextField(blank=True, null=True)
    skupina = MisencodedTextField()
    cetnost = MisencodedTextField(blank=True, null=True)
    pomucky = MisencodedTextField(blank=True, null=True)
    popis = MisencodedTextField()

    class Meta:
        db_table = 'hranicarkouzla'


    def __str__(self):
        return "{} od {}".format(
            self.jmeno,
            self.autor
        )


class WizardSpell(Creation):
    kouzsl = MisencodedTextField()
    mag = models.SmallIntegerField()
    magpop = MisencodedTextField()
    past = MisencodedTextField(blank=True, null=True)
    dosah = models.IntegerField(blank=True, null=True)
    dosahpop = MisencodedTextField(blank=True, null=True)
    rozsah = models.IntegerField()
    rozsahpop = MisencodedTextField(blank=True, null=True)
    vyvolani = models.IntegerField()
    vyvolanipop = MisencodedTextField()
    trvani = models.IntegerField()
    trvanipop = MisencodedTextField(blank=True, null=True)
    popis = MisencodedTextField()
    skupina = MisencodedTextField()

    class Meta:
        db_table = 'kouzla'

class Item(Creation):
    uc = MisencodedTextField(db_column='UC', blank=True, null=True)  # Field name made lowercase.
    kz = MisencodedCharField(db_column='KZ', max_length=3, blank=True, null=True)  # Field name made lowercase.
    delka = MisencodedCharField(max_length=3, blank=True, null=True)
    cena = models.IntegerField()
    popis = MisencodedTextField()
    malydostrel = models.IntegerField(blank=True, null=True)
    strednidostrel = models.IntegerField(blank=True, null=True)
    velkydostrel = models.IntegerField(blank=True, null=True)
    sfera = models.IntegerField(blank=True, null=True)
    vaha = models.IntegerField()
    skupina = MisencodedTextField()

    class Meta:
        db_table = 'predmety'

class DownloadItem(Creation):
    cesta = models.TextField(blank=True, null=True)
    format = models.TextField()
    popis = models.TextField()
    velikost = models.IntegerField()
    skupina = models.TextField()
    item = models.FileField(upload_to='soub', null=True)
    download_counter = models.IntegerField(default=0)

    class Meta:
        db_table = 'downloady'
        verbose_name_plural = 'Downloads'

class Quest(Creation):
    anotace = models.TextField()
    cesta = models.TextField(blank=True, null=True)
    klicsl = models.TextField()

    def get_final_url(self):
        return urljoin(urljoin(settings.QUEST_MEDIA_ROOT_URL, str(self.pk))+'/', self.cesta)

    class Meta:
        db_table = 'dobrodruzstvi'
