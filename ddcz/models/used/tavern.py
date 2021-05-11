from ddcz.models.used.users import UserProfile
from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField


class TavernTable(models.Model):
    jmeno = MisencodedCharField(unique=True, max_length=255)
    popis = MisencodedCharField(max_length=255)
    vlastnik = MisencodedCharField(max_length=30)
    povol_hodnoceni = MisencodedCharField(max_length=1)
    min_level = MisencodedCharField(max_length=1)
    zalozen = models.DateTimeField()
    verejny = MisencodedCharField(max_length=1)
    celkem = models.IntegerField(blank=True, null=True)
    sekce = models.IntegerField()

    @property
    def is_public(self):
        return self.verejny == "1"

    class Meta:
        db_table = "putyka_stoly"

    def is_user_access_allowed(self, user_profile, acls=None):
        # For ACL explanations, see TavernAccess
        # Note: Can't do "if not acls" since that would re-fetch for every empty set
        if acls is None:
            acls_models = self.tavernaccess_set.filter(
                nick_usera=user_profile.nick_uzivatele
            )
            acls = set([acl.typ_pristupu for acl in acls_models])

        if "vstza" in acls:
            return False
        elif self.is_public:
            return True
        elif "vstpo" in acls or "asist" in acls:
            return True
        else:
            return False


class TavernBookmark(models.Model):
    id_stolu = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    id_uz = models.ForeignKey(UserProfile, on_delete=models.CASCADE, db_column="id_uz")
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_book"
        unique_together = (("id_stolu", "id_uz"),)


class TavernTableLink(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_linku = models.IntegerField()

    class Meta:
        db_table = "putyka_linky"
        unique_together = (("id_stolu", "id_linku"),)


class TavernTableNoticeBoard(models.Model):
    id_stolu = models.IntegerField(unique=True)
    nazev_stolu = MisencodedCharField(max_length=128)
    text_nastenky = MisencodedTextField()
    posledni_zmena = models.DateTimeField(blank=True, null=True)
    zmenil = MisencodedCharField(max_length=25)

    class Meta:
        db_table = "putyka_nastenky"


class TavernComment(models.Model):
    id_stolu = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    text = MisencodedTextField()
    autor = MisencodedCharField(max_length=30)
    reputace = models.IntegerField()
    datum = models.DateTimeField()

    class Meta:
        db_table = "putyka_prispevky"


class TavernSection(models.Model):
    kod = models.IntegerField()
    poradi = models.IntegerField()
    nazev = MisencodedCharField(max_length=50)
    popis = MisencodedCharField(max_length=255)

    class Meta:
        db_table = "putyka_sekce"


class TavernAccess(models.Model):
    """
    Tavern access was used in v0. Used until old version shut down.
    Afterwards, it'll be preferred to store it as attributes in TavernTableVisitor
    """

    id_stolu = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    # typ_pristupu is essentially an enum:
    # vstpo = Allow access even if otherwise denied
    # vstza = Deny access even if otherwise allowed
    # asist = Assistent admin, allow access even if otherwise denied
    # zapis = Allow write access even if table is read only
    typ_pristupu = MisencodedCharField(max_length=5)
    nick_usera = MisencodedCharField(max_length=30)
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_pristup"
        unique_together = (("id_stolu", "typ_pristupu", "nick_usera"),)


class TavernTableVisitor(models.Model):
    """Tracking visits to a tavern table as well as bookmark status"""

    # TODO: Migrate to "table" and "user" attributes
    # :thinking: Shouldn't be too hard given we can leave the db_column in...
    id_stolu = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    id_uzivatele = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, db_column="id_uz"
    )
    ###
    # WARNING: oblibenost, sprava and pristup for access control are non-normative.
    # TavernBookmark, TavernAccess and IgnoredTavernTable are used instead.
    # We are going to migrate to those once old version is shut down.
    # See https://github.com/dracidoupe/graveyard/issues/237
    ###
    # 1: Tavern Table is bookmarked
    # 0: Tavern Table is not bookmarked, but this record is used for visit keeping
    # -1: Tavern Table is ignored and should not be displayed
    oblibenost = models.IntegerField(default=0)
    navstiveno = models.DateTimeField(blank=True, null=True)
    neprectenych = models.IntegerField(blank=True, null=True)
    # Boolean: 1 means user is an assistent admin
    sprava = models.IntegerField(default=0)
    # 2 = Allow write
    # 1 = Allow access
    # 0 = Behave as normal user
    # -2 = Deny access
    pristup = models.IntegerField(default=0)
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_uzivatele"
        unique_together = (("id_stolu", "id_uzivatele"),)


class IgnoredTavernTable(models.Model):
    id_uz = models.IntegerField()
    id_stolu = models.IntegerField()

    class Meta:
        managed = False
        db_table = "putyka_neoblibene"


###
# Deprecated Features
###
class TavernTableMerge(models.Model):
    id_ja = models.IntegerField()
    id_on = models.IntegerField()
    zustavam = models.SmallIntegerField()
    oznaceni = MisencodedCharField(max_length=60)

    class Meta:
        db_table = "putyka_slucovani"


class TavernVisit(models.Model):
    cas = models.DateTimeField(primary_key=True)
    misto = MisencodedCharField(max_length=31)
    pocet = models.IntegerField()

    class Meta:
        db_table = "putyka_navstevnost"
        unique_together = (("cas", "misto"),)
