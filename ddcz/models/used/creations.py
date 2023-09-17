# This module contains models that are acutally used in the current state
# of the application
# It still represents a "transitional" state needed to cooperate with
# the old application; hence do not grin at missing ForeignKeys and similar
# "rooms for improvement" that can be done once the original application
# is strangled out of its existence

from ddcz.creations import ApprovalChoices
import logging
from urllib.parse import urljoin

from django.apps import apps
from django.conf import settings
from django.db import models
from django.urls import reverse

from .users import UserProfile
from ..magic import MisencodedCharField, MisencodedTextField, MisencodedIntegerField
from ...text import create_slug

logger = logging.getLogger(__name__)


APPROVAL_CHOICES = (
    (ApprovalChoices.APPROVED.value, "Schváleno"),
    (ApprovalChoices.WAITING.value, "Neschváleno"),
)


EMPTY_SLUG_PLACEHOLDER = "dilo"


###
# Introduce an umbrella model for all Creations
###


class CreativePage(models.Model):
    """I represent a Creative Page as a first-item concept to help with foreign keys, definitions etc."""

    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    model_class = models.CharField(max_length=50)
    # editors = models.ManyToManyField(User)

    class Meta:
        verbose_name = "Rubrika"
        verbose_name_plural = "Rubriky"

    def __str__(self):
        return "Rubrika {}".format(
            self.name,
        )

    @classmethod
    def get_all_models(cls):
        models = []
        for page in cls.objects.all():
            app, model_class_name = page.model_class.split(".")
            model_class = apps.get_model(app, model_class_name)
            models.append({"model": model_class, "page": page})

        if len(models) == 0:
            raise ValueError("No models set up, run manage.py loaddata pages")

        return models

    def get_creation_canonical_url(self, creation):
        try:
            return reverse(
                "ddcz:creation-detail",
                kwargs={
                    "creative_page_slug": self.slug,
                    "creation_id": creation.pk,
                    "creation_slug": creation.get_slug(),
                },
            )
        except Exception:
            logger.error("Can't create slug, returning #")
            return "#"


# TODO: Not populated yet, not used, and under scrutiny
class CreativePageSection(models.Model):
    """Section within a Creative Page"""

    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)


class CreativePageConcept(models.Model):
    page = models.OneToOneField(CreativePage, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = "Koncept rubriky"
        verbose_name_plural = "Koncepty rubriky"

    def __str__(self):
        return "Koncept rubriky {}".format(
            self.page.name,
        )


class Author(models.Model):
    USER_TYPE = "u"
    WEBSITE_TYPE = "w"
    ANONYMOUS_USER_TYPE = "a"

    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    website = models.CharField(blank=True, null=True, max_length=255)
    website_email = models.CharField(blank=True, null=True, max_length=255)
    anonymous_user_nick = models.CharField(blank=True, null=True, max_length=255)
    user_nick = models.CharField(blank=True, null=True, max_length=255)

    author_type = models.CharField(
        max_length=1,
        choices=[
            (USER_TYPE, "Uživatel"),
            (WEBSITE_TYPE, "Webová Stránka"),
            (ANONYMOUS_USER_TYPE, "Anonymní Uživatel"),
        ],
        default=None,
    )

    def get_all_creations(self):
        """Returns a dictionary with all creations in the following format:
        {
            'creativepage_slug': {
                'creations': [CreationSubclassInstance]
                'page': [CreationPageInstance]
            }
        }

        Only creative pages where user published are included. Only approved creations
        are included in the result.
        """
        models = CreativePage.get_all_models()
        creations = {}

        for model_info in models:
            filters = {"author": self, "is_published": Creation.CREATION_APPROVED}
            if model_info["model"].SHARED_BETWEEN_CREATIVE_PAGES:
                filters["creative_page_slug"] = model_info["page"].slug

            page_creations = (
                model_info["model"].objects.filter(**filters).order_by("-published")
            )

            if len(page_creations) > 0:
                creations[model_info["page"].slug] = {
                    "creations": list(page_creations),
                    "page": model_info["page"],
                }

        return creations

    @property
    def name(self):
        if self.author_type == self.USER_TYPE:
            # This could potentially drop once author data is realiable
            # TODO: Verify nick updates propagate
            if self.user_nick:
                display_name = self.user_nick
            else:
                display_name = self.user.nick

        elif self.author_type == self.WEBSITE_TYPE:
            display_name = self.website
        elif self.author_type == self.ANONYMOUS_USER_TYPE:
            display_name = self.anonymous_user_nick
        else:
            raise AttributeError("Unknown type '%s'" % self.author_type)

        if not display_name:
            logger.error("MIGRATION_ERROR no display_name for author ID %s" % self.pk)
            display_name = "Neznámý"

        return display_name

    @property
    def slug(self):
        return create_slug(self.name)

    @property
    def profile_url(self):
        if self.author_type == self.WEBSITE_TYPE:
            display_name = "web"
        else:
            display_name = self.name

        return reverse(
            "ddcz:author-detail",
            kwargs={"author_id": self.pk, "slug": create_slug(display_name)},
        )

    def __str__(self):
        return self.name


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

    CREATION_APPROVED = "a"
    CREATION_NOT_APPROVED_YET = "n"
    # Flag to special-case handling of submodels shared beetween
    # multiple CreativePages -- see CommonArticle. For them,
    # filter based on `rubrika` attribute is needed
    SHARED_BETWEEN_CREATIVE_PAGES = False

    name = MisencodedTextField(db_column="jmeno")
    author_nick = MisencodedCharField(
        max_length=50, blank=True, null=True, db_column="autor"
    )
    author_mail = MisencodedCharField(
        max_length=50, blank=True, null=True, db_column="autmail"
    )
    is_published = MisencodedCharField(
        max_length=1, choices=APPROVAL_CHOICES, db_column="schvaleno"
    )
    original_web = MisencodedTextField(blank=True, null=True, db_column="zdroj")
    original_web_mail = MisencodedTextField(
        blank=True, null=True, db_column="zdrojmail"
    )
    rater_no = models.IntegerField(blank=True, null=True, db_column="pocet_hlasujicich")
    rating_sum = models.IntegerField(
        blank=True, null=True, db_column="hodnota_hlasovani"
    )
    rating = MisencodedIntegerField(max_length=5, db_column="pochvez")
    # dubious usage, probably used only by Quest, may be worth
    # removing in the future from other creations
    read = models.IntegerField(default=0, db_column="precteno")
    printed = models.IntegerField(default=0, db_column="tisknuto")
    published = models.DateTimeField(auto_now_add=True, db_column="datum")

    # Careful about difference from "Czech" `autor`, which is a text field
    # with a nickname that relies on being string equal with `UserProfile.nick_uzivatele`
    # Should be NOT NULL in the future, null allowed for transition period
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, blank=True, null=True  # , db_column="author"
    )

    # section = models.ForeignKey(CreativePageSection, on_delete=models.SET_NULL, null=True, blank=True)
    # Should be overwritten by models who want their legacy HTML checked
    legacy_html_attributes = []

    class Meta:
        abstract = True

    def get_author_profile(self):
        try:
            return UserProfile.objects.get(nick=self.author_nick)
        except UserProfile.DoesNotExist:
            return

    author_profile = property(get_author_profile)

    def get_slug(self):
        slug = create_slug(self.name)
        return slug or EMPTY_SLUG_PLACEHOLDER

    def get_canonical_url(self):
        if not getattr(self, "creative_page", None):
            raise ValueError(
                "`get_canonical_url` on a creation requires .creative_page attribute set. This will be remediated in the future, but currently there is not a lookup link from creations back to the model registry"
            )

        return self.creative_page.get_creation_canonical_url(self)

    def __str__(self):
        return "{} od {}".format(self.name, self.author_nick)


###
# Handle all models that should work with all creations.
# Do note that for backward compatibility, all relations to creations
# has to be NULLable and that (lazy) migration is needed in order to fix
# this model
###


class CreationVote(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, db_constraint=False, on_delete=models.CASCADE, db_column="id_uz"
    )
    # creation = models.OneToMany(Creation) -- to be introduced later
    creation_id = models.IntegerField(db_column="id_cizi")
    creative_page_slug = MisencodedCharField(max_length=20, db_column="rubrika")
    # 0-5 is normal rating of a creation
    # 8 denotes "rating deleted"
    rating = models.IntegerField(db_column="pochvez")
    time = models.IntegerField(db_column="time")
    # 0 or 1 for True/False; the vote can be changed only once
    changed = MisencodedCharField(max_length=1, db_column="opraveno")
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "hlasovani_prispevky"
        unique_together = (("user_profile", "creation_id", "creative_page_slug"),)

    @classmethod
    def get_creation_votes(cls, creative_page_slug, creation_id):
        return CreationVote.objects.filter(
            creative_page_slug=creative_page_slug, creation_id=creation_id, rating__lt=7
        ).select_related("user_profile")


###
# Particular models for all creations follow
###


class CommonArticle(Creation):
    """
    Represent "Common" article, covers a large proportion of site.
    It would be consistent to have subclasses per CreativePage, but that
    wouldn't map back to original structure.

    This is the only model that represents multiple CreativePages and hence
    needs to be special-cased for that purpose. Mapping to CreativePages
    is done based on `rubrika` attribute.
    """

    SHARED_BETWEEN_CREATIVE_PAGES = True

    text = MisencodedTextField(db_column="text")
    section = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="skupina"
    )
    abstract = MisencodedTextField(blank=True, null=True, db_column="anotace")
    creative_page_slug = MisencodedCharField(max_length=30, db_column="rubrika")

    legacy_html_attributes = ["text"]

    class Meta:
        db_table = "prispevky_dlouhe"
        verbose_name = "Běžné příspěvky"
        verbose_name_plural = "Běžné příspěvky"

    def __str__(self):
        return "{}: {} od {}".format(
            # COMMON_ARTICLES_CREATIVE_PAGES[self.rubrika]['name'],
            self.creative_page_slug,
            self.name,
            self.author_nick,
        )


class Monster(Creation):
    hitpoint_class = MisencodedTextField(
        db_column="zvt", verbose_name="Životaschopnost"
    )
    attack = MisencodedTextField(db_column="uc", verbose_name="Útočné číslo")
    defense = MisencodedTextField(db_column="oc", verbose_name="Obranné číslo")
    fortitude = MisencodedCharField(
        max_length=3, db_column="odl", verbose_name="Odolnost"
    )
    intelligence = MisencodedCharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="inteligence",
        verbose_name="Inteligence",
    )
    size = MisencodedCharField(max_length=20, db_column="vel", verbose_name="Velikost")
    vulnerability = MisencodedTextField(
        blank=True, null=True, db_column="zran", verbose_name="Zranitelnost"
    )
    agility = MisencodedTextField(
        blank=True, null=True, db_column="poh", verbose_name="Pohyblivost"
    )
    alignment = MisencodedTextField(
        blank=True, null=True, db_column="pres", verbose_name="Přesvědčení"
    )
    treasures = MisencodedTextField(
        blank=True, null=True, db_column="pokl", verbose_name="Poklady"
    )
    experience = MisencodedCharField(
        max_length=50, db_column="zkus", verbose_name="Zkušenost"
    )
    description = MisencodedTextField(db_column="popis", verbose_name="Popis")
    group = MisencodedTextField(db_column="skupina")
    combativeness = MisencodedCharField(
        max_length=50,
        blank=True,
        null=True,
        db_column="bojovnost",
        verbose_name="Bojovnost",
    )
    mental_strength = MisencodedCharField(
        db_column="SM", max_length=50, blank=True, null=True, verbose_name="Síla mysli"
    )

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "bestiar"
        verbose_name = "Nestvůra"
        verbose_name_plural = "Bestiář"

    def __str__(self):
        return "{} od {}".format(
            self.name,
            self.author_nick,
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

    image_path = MisencodedTextField(db_column="cesta", verbose_name="Cesta k obrázku")
    image_thumbnail_path = MisencodedTextField(
        db_column="cestathumb", verbose_name="Cesta k náhledovému obrázku"
    )

    class Meta:
        db_table = "galerie"

    def get_thumbnail_url(self):
        return urljoin(settings.GALLERY_MEDIA_ROOT_URL, self.image_thumbnail_path)

    def get_picture_url(self):
        return urljoin(settings.GALLERY_MEDIA_ROOT_URL, self.image_path)


class Photo(Creation):
    """See GalleryPicture; just part of different Creation Page"""

    image_path = MisencodedTextField(db_column="cesta", verbose_name="Cesta k obrázku")
    image_thumbnail_path = MisencodedTextField(
        db_column="cestathumb", verbose_name="Cesta k náhledovému obrázku"
    )

    class Meta:
        db_table = "fotogalerie"

    def get_thumbnail_url(self):
        return urljoin(settings.PHOTOGALLERY_MEDIA_ROOT_URL, self.image_thumbnail_path)

    def get_picture_url(self):
        return urljoin(settings.PHOTOGALLERY_MEDIA_ROOT_URL, self.image_path)


class Skill(Creation):
    attribute = MisencodedTextField(db_column="vlastnost", verbose_name="Vlastnost")
    difficulty = MisencodedTextField(db_column="obtiznost", verbose_name="Obtížnost")
    check_interval = MisencodedTextField(
        db_column="overovani", verbose_name="Ověřování"
    )
    total_success = MisencodedTextField(
        db_column="totuspech", verbose_name="Totální úspěch"
    )
    success = MisencodedTextField(db_column="uspech", verbose_name="Úspěch")
    failure = MisencodedTextField(db_column="neuspech", verbose_name="Neúspěch")
    fatal_failure = MisencodedTextField(
        db_column="fatneuspech", verbose_name="Fatální neúspěch"
    )
    description = MisencodedTextField(db_column="popis", verbose_name="Popis")
    group = MisencodedCharField(max_length=30, db_column="skupina")
    # TODO: No idea what this is used for, potentially drop
    voted = MisencodedTextField(blank=True, null=True, db_column="hlasoval")

    legacy_html_attributes = [
        "total_success",
        "success",
        "failure",
        "fatal_failure",
        "description",
    ]

    class Meta:
        db_table = "dovednosti"
        verbose_name = "Dovednost"
        verbose_name_plural = "Dovednosti"


class AlchemistTool(Creation):
    magenergy = models.IntegerField(
        blank=True, null=True, db_column="mag", verbose_name="Magenergie"
    )
    resources = models.SmallIntegerField(
        blank=True, null=True, db_column="suroviny", verbose_name="Suroviny"
    )
    base = MisencodedCharField(
        max_length=150, blank=True, null=True, db_column="zaklad", verbose_name="Základ"
    )
    discovery = MisencodedCharField(
        max_length=150,
        blank=True,
        null=True,
        db_column="nalezeni",
        verbose_name="Nalezení",
    )
    duration = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="trvani", verbose_name="Trvání"
    )
    crafting = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="vyroba", verbose_name="Výroba"
    )
    dangerousness = MisencodedCharField(
        max_length=30,
        blank=True,
        null=True,
        db_column="nebezpecnost",
        verbose_name="Nebezpečnost",
    )
    strength = MisencodedCharField(
        max_length=30, blank=True, null=True, db_column="sila", verbose_name="Síla"
    )
    color_taste_smell = MisencodedCharField(
        max_length=30,
        blank=True,
        null=True,
        db_column="bcz",
        verbose_name="Barva/chuť/zápach:",
    )
    daily_magenergy = models.IntegerField(
        blank=True, null=True, db_column="denmag", verbose_name="Magy/den"
    )
    effect_outreach = MisencodedCharField(
        max_length=20,
        blank=True,
        null=True,
        db_column="dosah_ucinku",
        verbose_name="Dosah účinku",
    )
    crafter_level = MisencodedCharField(
        max_length=10,
        null=True,
        blank=True,
        db_column="uroven_vyrobce",
        verbose_name="Úroveň výrobce",
    )
    plane = MisencodedCharField(
        max_length=20, null=True, blank=True, db_column="sfera", verbose_name="Sféra"
    )
    description = MisencodedTextField(db_column="popis", verbose_name="Popis")
    group = MisencodedCharField(
        max_length=30, db_column="skupina", verbose_name="Skupina"
    )

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "alchpredmety"
        verbose_name = "Alchymistický předmět"
        verbose_name_plural = "Alchimistické předměty"

    def __str__(self):
        return "{} od {}".format(
            self.name,
            self.author_nick,
        )


class Link(models.Model):
    name = MisencodedTextField(db_column="nazev")
    url = MisencodedTextField(db_column="adresa")
    description = MisencodedTextField(db_column="popis")
    rating = MisencodedCharField(max_length=1, db_column="pochvez")
    is_approved = MisencodedCharField(
        max_length=1, choices=APPROVAL_CHOICES, db_column="schvaleno"
    )
    published = models.DateTimeField(db_column="datum")
    rater_no = models.IntegerField(blank=True, null=True, db_column="pocet_hlasujicich")
    rater_sum = models.IntegerField(
        blank=True, null=True, db_column="hodnota_hlasovani"
    )

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "linky"
        verbose_name = "Odkaz"
        verbose_name_plural = "Odkazy"

    def __str__(self):
        return "{} {}".format(self.name, self.url)


class RangerSpell(Creation):
    magenergy = models.SmallIntegerField(db_column="mag", verbose_name="Magenergie")
    magenergy_description = MisencodedTextField(db_column="magpop", verbose_name="")
    reach = models.IntegerField(
        blank=True, null=True, db_column="dosah", verbose_name="Rozsah"
    )
    reach_description = MisencodedTextField(
        blank=True, null=True, db_column="dosahpop", verbose_name=""
    )
    extent = models.IntegerField(
        blank=True, null=True, db_column="rozsah", verbose_name="Rozsah"
    )
    extent_description = MisencodedTextField(
        blank=True, null=True, db_column="rozsahpop", verbose_name=""
    )
    invocation = models.IntegerField(
        blank=True, null=True, db_column="vyvolani", verbose_name="Vyvolání"
    )
    invocation_description = MisencodedTextField(
        blank=True, null=True, db_column="vyvolanipop", verbose_name=""
    )
    spell_type = MisencodedTextField(
        blank=True, null=True, db_column="druh", verbose_name="Druh"
    )
    frequency = MisencodedTextField(
        blank=True, null=True, db_column="cetnost", verbose_name="Četnost"
    )
    tools = MisencodedTextField(
        blank=True, null=True, db_column="pomucky", verbose_name="Pomůcky"
    )
    description = MisencodedTextField(db_column="popis", verbose_name="Popis")
    group = MisencodedTextField(db_column="skupina", verbose_name="Skupina")

    legacy_html_attributes = ["description", "tools"]

    class Meta:
        db_table = "hranicarkouzla"

    def __str__(self):
        return "{} od {}".format(self.name, self.author_nick)


class WizardSpell(Creation):
    summon_words = MisencodedTextField(
        db_column="kouzsl", verbose_name="Kouzelná slova"
    )
    magenergy = models.SmallIntegerField(db_column="mag", verbose_name="Magenergie")
    magenergy_description = MisencodedTextField(db_column="magpop", verbose_name="")
    skill_check = MisencodedTextField(
        blank=True, null=True, db_column="past", verbose_name="Past"
    )
    reach = models.IntegerField(
        blank=True, null=True, db_column="dosah", verbose_name="Rozsah"
    )
    reach_description = MisencodedTextField(
        blank=True, null=True, db_column="dosahpop", verbose_name=""
    )
    extent = models.SmallIntegerField(
        blank=True, null=True, db_column="rozsah", verbose_name="Rozsah"
    )
    extent_description = MisencodedTextField(
        blank=True, null=True, db_column="rozsahpop", verbose_name=""
    )
    invocation = models.SmallIntegerField(db_column="vyvolani", verbose_name="Vyvolání")
    invocation_description = MisencodedTextField(
        db_column="vyvolanipop", verbose_name=""
    )
    duration = models.IntegerField(db_column="trvani", verbose_name="Trvání")
    duration_description = MisencodedTextField(
        blank=True, null=True, db_column="trvanipop", verbose_name=""
    )
    description = MisencodedTextField(db_column="popis")
    group = MisencodedTextField(db_column="skupina")

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "kouzla"
        verbose_name = "Kouzelnické kouzlo"
        verbose_name_plural = "Kouzelnická kouzla"


class Item(Creation):
    attack_number = MisencodedTextField(
        db_column="UC", blank=True, null=True, verbose_name="Síla zbraně"
    )
    armour_quality = MisencodedCharField(
        db_column="KZ",
        max_length=3,
        blank=True,
        null=True,
        verbose_name="Kvalita zbroje",
    )
    length = MisencodedCharField(
        max_length=3, blank=True, null=True, db_column="delka", verbose_name="Délka"
    )
    price = models.IntegerField(db_column="cena", verbose_name="Cena")
    range_small = models.IntegerField(
        blank=True, null=True, db_column="malydostrel", verbose_name="Malý dostřel"
    )
    range_expected = models.IntegerField(
        blank=True,
        null=True,
        db_column="strednidostrel",
        verbose_name="Střední dostřel",
    )
    range_long = models.IntegerField(
        blank=True, null=True, db_column="velkydostrel", verbose_name="Velký dostřel"
    )
    sphere = models.IntegerField(
        blank=True, null=True, db_column="sfera", verbose_name="Sféra"
    )
    weight = models.IntegerField(db_column="vaha", verbose_name="Váha")
    description = MisencodedTextField(db_column="popis", verbose_name="Popis")
    group = MisencodedTextField(db_column="skupina")

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "predmety"
        verbose_name = "Předmět"
        verbose_name_plural = "Předměty"


class DownloadItem(Creation):
    path = models.TextField(blank=True, null=True, db_column="cesta")
    format = models.TextField(db_column="format")
    description = models.TextField(db_column="popis")
    size = models.IntegerField(db_column="velikost")
    group = models.TextField(db_column="skupina")
    item = models.FileField(upload_to="soub", null=True, db_column="item")
    download_counter = models.IntegerField(default=0, db_column="download_counter")

    legacy_html_attributes = ["description"]

    class Meta:
        db_table = "downloady"
        verbose_name_plural = "Downloads"


class Quest(Creation):
    abstract = models.TextField(db_column="anotace")
    path = models.TextField(blank=True, null=True, db_column="cesta")
    keywords = models.TextField(db_column="klicsl")

    def get_final_url(self):
        return urljoin(
            urljoin(settings.QUEST_MEDIA_ROOT_URL, str(self.pk)) + "/", self.path
        )

    class Meta:
        db_table = "dobrodruzstvi"
