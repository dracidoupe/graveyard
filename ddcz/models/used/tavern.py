from copy import deepcopy
from enum import Enum, unique
from itertools import chain

from ddcz.models.used.users import UserProfile
from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField

TAVERN_SECTION_PRIVATE_ID = 19
TAVERN_SECTION_NEW_ID = 3
TAVERN_SECTION_ARCHIVE_ID = 18


@unique
class TavernAccessRights(Enum):
    ACCESS_ALLOWED = "vstpo"
    WRITE_ALLOWED = "zapis"
    ACCESS_BANNED = "vstza"
    ASSISTANT_ADMIN = "asist"
    DEFAULT = None


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
        if user_profile.nick_uzivatele == self.vlastnik:
            return True

        if acls is None:
            acls_models = self.tavernaccess_set.filter(
                nick_usera=user_profile.nick_uzivatele
            )
            acls = set([acl.typ_pristupu for acl in acls_models])

        if "asist" in acls:
            return True
        if "vstza" in acls:
            return False
        elif self.is_public:
            return True
        elif "vstpo" in acls:
            return True
        else:
            return False

    def update_access_privileges(
        self,
        access_banned=None,
        access_allowed=None,
        write_allowed=None,
        assistant_admins=None,
    ):
        """
        Set access privileges to new versions described by arguments. All lists are list of IDs.
        If None is given, it means "do not update given list of privileges"
        If empty list is given ([]), it means "set this access type to none.
        """
        # We can migrate to upsert syntax if we'd migrate to postgres
        # Normally, I'd just delete & insert, but given the presence of django_id,
        # let's try to be a bit smarter

        ###
        # First, the normative version
        ###
        unprocessed_access_map = {}
        # TODO: not needed, unprocessed_access_map.keys() is enough
        processing_privileges = set()

        if access_allowed is not None:
            unprocessed_access_map[TavernAccessRights.ACCESS_ALLOWED] = set(
                access_allowed
            )
            processing_privileges.add(TavernAccessRights.ACCESS_ALLOWED)
        if write_allowed is not None:
            unprocessed_access_map[TavernAccessRights.WRITE_ALLOWED] = set(
                write_allowed
            )
            processing_privileges.add(TavernAccessRights.WRITE_ALLOWED)
        if access_banned is not None:
            unprocessed_access_map[TavernAccessRights.ACCESS_BANNED] = set(
                access_banned
            )
            processing_privileges.add(TavernAccessRights.ACCESS_BANNED)
        if assistant_admins is not None:
            unprocessed_access_map[
                TavernAccessRights.ASSISTANT_ADMIN
            ] = assistant_admins
            processing_privileges.add(TavernAccessRights.ASSISTANT_ADMIN)

        self.update_legacy_privileges(
            unprocessed_access_map=unprocessed_access_map,
            processing_privileges=processing_privileges,
        )
        self.update_future_privileges(
            unprocessed_access_map=unprocessed_access_map,
            processing_privileges=processing_privileges,
        )

    def update_legacy_privileges(self, unprocessed_access_map, processing_privileges):
        """
        Update records in TavernAccess table to reflect the access map given.

        Algorithm:

        * Get all access rights for the access types we are processing
        * Figure out which rights were added and which deleted
            (leaving the ones that are the same untouched in the database)
        * Add new privileges
        * Drop the deleted ones
        """
        # Copy as we are using it as processing queue and it needs to be reatined
        # for updating future privileges
        access_map = deepcopy(unprocessed_access_map)
        table_acls_to_delete = []
        table_acls_models = self.tavernaccess_set.filter(
            typ_pristupu__in=[p.value for p in processing_privileges]
        )
        # Diff in-database ACLs agaist the new set
        # Not in new set = delete from db; is in new set = leave untouched
        for acl in table_acls_models:
            access_type = TavernAccessRights(acl.typ_pristupu)
            if acl.pk not in access_map[access_type]:
                table_acls_to_delete.append(acl.pk)

            access_map[access_type].remove(acl.pk)

        # Adding new privileges
        for access_type in access_map:
            for user_id in access_map[access_type]:
                TavernAccess.objects.create(
                    id_stolu=self,
                    typ_pristupu=access_type.value,
                    nick_usera=UserProfile.objects.get(pk=user_id).nick_uzivatele,
                )

        # Deleting the ones that were dropped
        TavernAccess.objects.filter(django_id__in=table_acls_to_delete).delete()

    def update_future_privileges(self, unprocessed_access_map, processing_privileges):
        """
        Update TableVisitor to reflect the access map given.
        See the problem with definitions: https://github.com/dracidoupe/graveyard/issues/260

        Algorithm:

        * Get all table visitors with new access defined
        * Reset access of all visitors who has any access of processing_privileges defined
        * Go through unprocessed access map, update preselected visitors and insert the rest
        """
        # Strictly not necessary as long as the call order is upheld; kill with single-source-of-access-truth refactoring
        access_map = deepcopy(unprocessed_access_map)
        all_affected_users = set(chain(*access_map.values()))

        visitors = list(
            TavernTableVisitor.objects.filter(id_uzivatele__in=all_affected_users)
        )
        visitors_map = {visitor.pk: visitor for visitor in visitors}

        # First, reflect privileges that were dropped
        # TODO: This can be simplified in the future, but now be more careful: reset access
        # of all visitors per access type
        for privilege in processing_privileges:
            if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                TavernTableVisitor.objects.filter(
                    id_stolu=self,
                    pristup=TavernTableVisitor.ACCESS_CODE_MAP[privilege],
                ).exclude(id_uzivatele_id__in=all_affected_users).update(
                    pristup=TavernTableVisitor.ACCESS_CODE_MAP[
                        TavernAccessRights.DEFAULT
                    ]
                )
            elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                TavernTableVisitor.objects.filter(id_stolu=self, sprava=1).exclude(
                    id_uzivatele_id__in=all_affected_users
                ).update(sprava=0)
            else:
                raise ValueError(f"Encountered unknown privilege {privilege}")

        # Next, reflect updated and added privileges
        for privilege in access_map:
            for user_id in access_map[privilege]:
                # Update to the user with either existing privileges or at least a tavern table visit
                if user_id in visitors_map:
                    visitor = visitors_map[user_id]

                    if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                        visitor.pristup = visitor.ACCESS_CODE_MAP[privilege]
                    elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                        visitor.sprava = 1

                    visitor.save()
                else:
                    args = {
                        "id_stolu": self,
                        "id_uzivatele_id": user_id,
                    }
                    if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                        args["pristup"] = TavernTableVisitor.ACCESS_CODE_MAP[privilege]
                    elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                        args["sprava"] = 1

                    visitor = TavernTableVisitor.objects.create(**args)
                    # for handling situations like access allowed *and* assistant admin
                    visitors.append(visitor)
                    visitors_map[user_id] = visitor


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

    ACCESS_CODE_MAP = {
        TavernAccessRights.ACCESS_ALLOWED: 1,
        TavernAccessRights.ACCESS_BANNED: -2,
        TavernAccessRights.WRITE_ALLOWED: 2,
        TavernAccessRights.DEFAULT: 0,
    }

    class Meta:
        db_table = "putyka_uzivatele"
        unique_together = (("id_stolu", "id_uzivatele"),)


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


class IgnoredTavernTable(models.Model):
    id_uz = models.IntegerField()
    id_stolu = models.IntegerField()

    class Meta:
        managed = False
        db_table = "putyka_neoblibene"


class TavernAccess(models.Model):
    """Tavern access was used in v0. Now it's preferred to store it as attributes in TavernTableVisitor"""

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
