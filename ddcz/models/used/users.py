from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from django.contrib.auth.models import User

from ...text import create_slug
from ..magic import MisencodedCharField


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
    # This is an important field! It lists which fields can be publicly displayed. The format of the fields
    # is CSV with implied field names. The order of the fields is:
    #   jmeno, prijmeni, email, ICQ, pohlavi, vek, kraj, narozeniny
    # The actual records looks like this:
    #   ,,,,,,,1
    # meaning "show birthday and nothing else"
    # Note that last two fields were added later on, meaning records with less than eight fields can occur, like this:
    #   ,,,,,,
    vypsat_udaje = MisencodedCharField(max_length=15)
    ikonka_uzivatele = MisencodedCharField(max_length=25, blank=True, null=True)
    popis_uzivatele = MisencodedCharField(max_length=255, blank=True, null=True)
    nova_posta = models.IntegerField(default=0)
    skin = MisencodedCharField(max_length=10)
    reputace = models.IntegerField(default=0)
    reputace_rozdel = models.PositiveIntegerField(default=0)
    status = MisencodedCharField(max_length=1)
    reg_schval_datum = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    indexhodnotitele = models.DecimalField(
        max_digits=4, decimal_places=2, default=-99.99
    )
    reload = MisencodedCharField(max_length=1)
    max_level = models.IntegerField(blank=True, null=True)
    api_key = MisencodedCharField(unique=True, max_length=40, blank=True, null=True)
    tavern_bookmarks = models.ManyToManyField(
        "TavernTable", through="TavernBookmark", through_fields=("id_uz", "id_stolu")
    )

    class Meta:
        db_table = "uzivatele"

    @property
    def slug(self):
        slug = create_slug(self.nick_uzivatele)
        if not slug:
            slug = "neznamy"
            # TODO: log an error
        return slug

    @property
    def icon_url(self):
        if not self.ikonka_uzivatele:
            return None
        else:
            return urljoin(settings.USER_ICON_MEDIA_ROOT_URL, self.ikonka_uzivatele)

    @property
    def is_author(self):
        return self.author is not None

    @property
    def is_female(self):
        return self.pohlavi_uzivatele in ["Žena", "®ena"]

    @property
    def author_url(self):
        return self.author.profile_url

    @property
    def nick(self):
        return self.nick_uzivatele

    @property
    def age(self):
        return self.vek_uzivatele

    @property
    def location(self):
        return self.kraj_uzivatele

    @property
    def description(self):
        return self.popis_uzivatele or ""

    @property
    def profile_url(self):
        return reverse(
            "ddcz:user-detail",
            kwargs={"user_profile_id": self.pk, "nick_slug": self.slug},
        )

    @property
    def registration_date(self):
        try:
            return self.reg_schval_datum.strftime("%-d. %-m. %Y v %-H:%M")
        except ValueError:
            return self.reg_schval_datum.strftime("%d. %m. %Y v %H:%M")

    @property
    def last_login(self):
        try:
            return self.pospristup.strftime("%-d. %-m. %Y v %-H:%M")
        except ValueError:
            return self.pospristup.strftime("%d. %m. %Y v %H:%M")

    @property
    def public_listing_permissions(self):
        """Load permissions from the field, parse it and return as list of boolean values"""
        # TODO: Once we are doing field renaming, this should be normalized towards field names
        if not self.vypsat_udaje:
            permissions = [""] * 8
        else:
            permissions = self.vypsat_udaje.split(",")
        return {
            "jmeno": permissions[0] == "1",
            "prijmeni": permissions[1] == "1",
            "email": permissions[2] == "1",
            "icq": permissions[3] == "1",
            "pohlavi": permissions[4] == "1",
            "vek": permissions[5] == "1",
            "kraj": len(permissions) > 6 and permissions[6] == "1",
            "narozeniny": len(permissions) > 7 and permissions[7] == "1",
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
    parametr = MisencodedCharField(primary_key=True, max_length=40)
    hodnota = MisencodedCharField(max_length=30)

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
    id_zaznamu = models.AutoField(primary_key=True)
    nick_uzivatele = models.CharField(unique=True, max_length=30)
    email = models.CharField(unique=True, max_length=40)
    jmeno = models.CharField(max_length=40)
    prijmeni = models.CharField(max_length=40)
    pohlavi = models.CharField(max_length=4)
    datum = models.IntegerField()
    patron = models.IntegerField()
    primluvy = models.IntegerField()
    osloveni = models.CharField(max_length=50, blank=True, null=True)
    popis_text = models.TextField()

    class Meta:
        db_table = "uzivatele_cekajici"
        unique_together = (("jmeno", "prijmeni"),)
