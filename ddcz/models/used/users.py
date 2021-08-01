from time import time
from urllib.parse import urljoin

from django.conf import settings
from django.core.checks.messages import Error
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from django.contrib.auth.models import User

from ...text import create_slug
from ..magic import MisencodedCharField

APPROVAL_TIME = 24 * 60 * 60

LEVEL_DESCRIPTIONS = {
    "0": """
            Jsi klasickým uživatelem webu doupěte, který tu a tam něco
            okomentuje, rád se podívá na díla a správně si žije pod
            krásným žlutým Sluncem.
         """,
    "1": """
            Již tě nebavilo stále jen sledovat žluté Slunce, a tak došlo
            na pádná slova a hromové argumenty! Křik se rozléhá hospodou,
            jak teče azurová krev diskuzních protivníků!
         """,
    "2": """
            Ne, že bys nebyl tuhým soupeřem pro jednoho diskutéra,
            ale dokážeš napsat i srozumitelnější příspěvky,
            a to správnou barvou modrého pera, tou správnou, kterou se
            píší recenze a kritiky.
         """,
    "3": """
            Na rozdíl od svých kolegů, kteří píší do diskuzí a hodnotí
            díla, ty skutečně díla vytváříš! Tvoje kreativita tě sice
            občas vytočí do oranžova, ale taková práce zaslouží odměnu.
         """,
    "4": """
            Už je to chvíle, co se tvá kreativita projevuje naplno,
            moudrost a zkušenosti tě vedou k vytváření velmi kvalitních
            prací. Je pravda, že barva 4 a více hvězd na fialovém plášti
            čaroděje by ještě chtěla doplnit o noblesní okraj, ale už i
            tak je dílem takřka dokonalosti.
         """,
    "5": """
            Západ Slunce při správném počasí nese barvu červena. Stejně
            jako závěr každého dne, kde je již všechno práce odvedena,
            i ty máš za sebou pořádnou nálož zásluh. Proto si užívej
            nádherné zapadající Slunce i další den, a to napořád
            s připomínkou, že jsme vděčni.
         """,
    "8": """
            Zelená znamená kupředu! Opravuj! Kritizuj! Vytvářej!
            Řiď a zpívej píseň, která tě povede na cestách mezi
            diskutéry, tvůrci, kamarády, ale i spamery a zločince.
            Trestej a odměňuj! Tvá magická moc je nezměrná,
            využívej ji moudře, soudče z řad nejvyšších.
         """,
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    nick = MisencodedCharField(unique=True, max_length=25, db_column="nick_uzivatele")
    name_given = MisencodedCharField(max_length=20, db_column="jmeno_uzivatele")
    name_family = MisencodedCharField(max_length=20, db_column="prijmeni_uzivatele")
    password_v1 = MisencodedCharField(max_length=40, db_column="psw_uzivatele")
    email = MisencodedCharField(max_length=50, db_column="email_uzivatele")
    gender = MisencodedCharField(
        max_length=4, blank=True, null=True, db_column="pohlavi_uzivatele"
    )
    age = models.IntegerField(default=0, db_column="vek_uzivatele")
    shire = MisencodedCharField(max_length=20, db_column="kraj_uzivatele")
    chat_color = MisencodedCharField(max_length=6, db_column="chat_barva")
    chat_font = models.IntegerField(default=12, db_column="chat_pismo")
    chat_reload = models.IntegerField(default=15, db_column="chat_reload")
    chat_message_no = models.IntegerField(default=20, db_column="chat_zprav")
    chat_filter = MisencodedCharField(
        max_length=255, blank=True, null=True, db_column="chat_filtr"
    )
    chat_filter_display = models.IntegerField(
        default=0, db_column="chat_filtr_zobrazit"
    )
    last_login = models.DateTimeField(auto_now_add=True, db_column="pospristup")
    level = MisencodedCharField(max_length=1, db_column="level")
    icq = models.IntegerField(default=0, db_column="icq_uzivatele")
    # This is an important field! It lists which fields can be publicly displayed. The format of the fields
    # is CSV with implied field names. The order of the fields is:
    #   jmeno, prijmeni, email, ICQ, pohlavi, vek, kraj, narozeniny
    # The actual records looks like this:
    #   ,,,,,,,1
    # meaning "show birthday and nothing else"
    # Note that last two fields were added later on, meaning records with less than eight fields can occur, like this:
    #   ,,,,,,
    pii_display_permissions = MisencodedCharField(
        max_length=15, db_column="vypsat_udaje"
    )
    icon = MisencodedCharField(
        max_length=25, blank=True, null=True, db_column="ikonka_uzivatele"
    )
    description_raw = MisencodedCharField(
        max_length=255, blank=True, null=True, db_column="popis_uzivatele"
    )
    new_post_no = models.IntegerField(default=0, db_column="nova_posta")
    skin = MisencodedCharField(max_length=10, db_column="skin")
    reputation = models.IntegerField(default=0, db_column="reputace")
    reputation_available = models.PositiveIntegerField(
        default=0, db_column="reputace_rozdel"
    )
    status = MisencodedCharField(max_length=1, db_column="status")
    registration_approved_date = models.DateTimeField(
        blank=True, null=True, auto_now_add=True, db_column="reg_schval_datum"
    )
    evaluator_index = models.DecimalField(
        max_digits=4, decimal_places=2, default=-99.99, db_column="indexhodnotitele"
    )
    reload = MisencodedCharField(max_length=1, db_column="reload")
    max_level = models.IntegerField(blank=True, null=True, db_column="max_level")
    api_key = MisencodedCharField(unique=True, max_length=40, blank=True, null=True)
    tavern_bookmarks = models.ManyToManyField(
        "TavernTable",
        through="TavernBookmark",
        through_fields=("user_profile", "tavern_table"),
    )

    class Meta:
        db_table = "uzivatele"

    @property
    def slug(self):
        slug = create_slug(self.nick)
        if not slug:
            slug = "neznamy"
            # TODO: log an error
        return slug

    @property
    def icon_url(self):
        if not self.icon:
            return None
        else:
            return urljoin(settings.USER_ICON_MEDIA_ROOT_URL, self.icon)

    @property
    def is_author(self):
        return self.author is not None

    @property
    def is_female(self):
        return self.gender in ["Žena", "®ena"]

    @property
    def author_url(self):
        return self.author.profile_url

    @property
    def name(self):
        return f"{self.name_given} {self.name_family}"

    @property
    def location(self):
        return self.shire

    @property
    def description(self):
        return self.description_raw or ""

    @property
    def profile_url(self):
        return reverse(
            "ddcz:user-detail",
            kwargs={"user_profile_id": self.pk, "nick_slug": self.slug},
        )

    @property
    def registration_date(self):
        return self.registration_approved_date

    @property
    def public_listing_permissions(self):
        """Load permissions from the field, parse it and return as list of boolean values"""
        # TODO: Once we are doing field renaming, this should be normalized towards field names
        if not self.pii_display_permissions:
            permissions = [""] * 8
        else:
            permissions = self.pii_display_permissions.split(",")
        return {
            "name_given": permissions[0] == "1",
            "name_family": permissions[1] == "1",
            "email": permissions[2] == "1",
            "icq": permissions[3] == "1",
            "gender": permissions[4] == "1",
            "age": permissions[5] == "1",
            "shire": len(permissions) > 6 and permissions[6] == "1",
            "birthday": len(permissions) > 7 and permissions[7] == "1",
        }

    @property
    def show_email(self):
        return self.public_listing_permissions["email"]


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


class LevelSystemParams(models.Model):
    parametr = MisencodedCharField(primary_key=True, max_length=40, db_column="")
    hodnota = MisencodedCharField(max_length=30, db_column="")

    class Meta:
        db_table = "level_parametry_2"


class MentatNewbie(models.Model):
    """
    Handle a relationship between two UserProfiles: a mentat and a newbie.

    In theory, this could be generated using ManyToManyField:
    https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/

    In practice, Django doesn't allow attributes on the relationship, hence we need
    to hack around with a dedicated model anyway.
    """

    # Note: newbie_id is NOT a primary key, but this is how Django model framework
    # inspected the DB. Happens because Django doesn't support composite primary keys
    # newbie_id = models.IntegerField()
    # mentat_id = models.IntegerField()
    newbie = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="newbies",
        db_column="newbie_id",
        db_constraint=False,
    )
    mentat = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="mentats",
        db_column="mentat_id",
        db_constraint=False,
    )
    newbie_rate = models.IntegerField()
    mentat_rate = models.IntegerField()
    locked = MisencodedCharField(max_length=2)
    penalty = models.IntegerField()
    # This field is not needed except for Django to be happy as it doesn't support
    # composite primary keys
    # TODO: This is added without a primary key to allow prefilling data on
    # production and to allow to migrate to primary key later
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "mentat_newbie"
        unique_together = (("newbie", "mentat"),)


class UzivateleCekajici(models.Model):
    id = models.AutoField(primary_key=True, db_column="id_zaznamu")
    nick = models.CharField(unique=True, max_length=30, db_column="nick_uzivatele")
    email = models.CharField(unique=True, max_length=40, db_column="email")
    name_given = models.CharField(max_length=40, db_column="jmeno")
    name_family = models.CharField(max_length=40, db_column="prijmeni")
    gender = models.CharField(max_length=4, db_column="pohlavi")
    date = models.IntegerField(db_column="datum")
    patron = models.IntegerField(db_column="patron")
    supporters = models.IntegerField(db_column="primluvy")
    salutation = models.CharField(
        max_length=50, blank=True, null=True, db_column="osloveni"
    )
    description = models.TextField(db_column="popis_text")

    class Meta:
        db_table = "uzivatele_cekajici"
        unique_together = (("name_given", "name_family"),)

    @property
    def patron_name(self):
        return UserProfile.objects.get(id=self.patron).nick

    @property
    def waiting_time(self):
        time_now = int(time())
        time_diff = time_now - self.date
        return time_diff

    @property
    def expected_approval_time(self):
        return self.date + APPROVAL_TIME

    def patronize(self, patron_id):
        try:
            self.patron = patron_id
            self.save()
        except:
            raise Error(
                "The user could not be saved as a patron to awaiting registration."
            )
        return True
