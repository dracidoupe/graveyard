from copy import deepcopy
from enum import Enum, unique
from itertools import chain

from django.db import models

from .users import UserProfile
from ..magic import MisencodedCharField, MisencodedTextField
from ...text import misencode

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
    name = MisencodedCharField(unique=True, max_length=255, db_column="jmeno")
    description = MisencodedCharField(max_length=255, db_column="popis")
    owner = MisencodedCharField(max_length=30, db_column="vlastnik")
    # TODO: MisencodedBooleanField
    allow_rep = MisencodedCharField(max_length=1, db_column="povol_hodnoceni")
    min_level = MisencodedCharField(max_length=1, db_column="min_level")
    created = models.DateTimeField(db_column="zalozen")
    # TODO: MisencodedBooleanField
    public = MisencodedCharField(max_length=1, db_column="verejny")
    posts_no = models.IntegerField(blank=True, null=True, db_column="celkem")
    # TODO: FK migration
    section = models.IntegerField(db_column="sekce")

    @property
    def is_public(self):
        return self.public == "1"

    class Meta:
        db_table = "putyka_stoly"

    def show_listing_link(self, *args, **kwargs):
        return self.is_user_access_allowed(*args, **kwargs)

    def is_user_write_allowed(self, user_profile, acls=None):
        # For ACL explanations, see TavernAccess
        if user_profile.nick == self.owner:
            return True

        # Note: Can't do "if not acls" since that would re-fetch for every empty set
        if acls is None:
            acls = self.get_user_acls(user_profile)

        # User can't write if they can't even enter
        if not self.is_user_access_allowed(user_profile, acls=acls):
            return False

        if not self.is_write_restricted():
            return True
        else:
            return TavernAccessRights.WRITE_ALLOWED in acls

    def is_user_access_allowed(self, user_profile, acls=None):
        # For ACL explanations, see TavernAccess
        if user_profile.nick == self.owner:
            return True

        # Note: Can't do "if not acls" since that would re-fetch for every empty set
        if acls is None:
            acls = self.get_user_acls(user_profile)

        if TavernAccessRights.ASSISTANT_ADMIN in acls:
            return True
        if TavernAccessRights.ACCESS_BANNED in acls:
            return False
        elif self.is_public:
            return True
        elif TavernAccessRights.ACCESS_ALLOWED in acls:
            return True
        else:
            return False

    def is_notice_board_update_allowed(self, user_profile, acls=None):
        # For ACL explanations, see TavernAccess
        if user_profile.nick == self.owner:
            return True

        # Note: Can't do "if not acls" since that would re-fetch for every empty set
        if acls is None:
            acls = self.get_user_acls(user_profile)

        if TavernAccessRights.ASSISTANT_ADMIN in acls:
            return True

        return False

    def is_write_restricted(self):
        # FIXME: Looking this up should be an attribute, not a query
        # see #297 <https://github.com/dracidoupe/graveyard/issues/297>
        # Meanwhile, this can be annotated in a view, thus look it up
        if getattr(self, "write_allowed_user_no", None):
            return self.write_allowed_user_no > 0
        else:
            self.tavernaccess_set.filter(
                access_type=TavernAccessRights.WRITE_ALLOWED
            ).count() > 0

    def get_user_acls(self, user_profile):
        acls_models = self.tavernaccess_set.filter(
            user_nick=misencode(user_profile.nick)
        )
        return set([TavernAccessRights(acl.access_type) for acl in acls_models])

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
        If empty list is given ([]), it means "set this access type to no user.
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
            access_type__in=[p.value for p in processing_privileges]
        )
        # Diff in-database ACLs agaist the new set
        # Not in new set = delete from db; is in new set = leave untouched
        for acl in table_acls_models:
            access_type = TavernAccessRights(acl.access_type)
            if acl.pk not in access_map[access_type]:
                table_acls_to_delete.append(acl.pk)

            access_map[access_type].remove(acl.pk)

        # Adding new privileges
        for access_type in access_map:
            for user_id in access_map[access_type]:
                TavernAccess.objects.create(
                    tavern_table=self,
                    access_type=access_type.value,
                    user_nick=UserProfile.objects.get(pk=user_id).nick,
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
            TavernTableVisitor.objects.filter(user_profile_id__in=all_affected_users)
        )
        visitors_map = {visitor.pk: visitor for visitor in visitors}

        # First, reflect privileges that were dropped
        # TODO: This can be simplified in the future, but now be more careful: reset access
        # of all visitors per access type
        for privilege in processing_privileges:
            if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                TavernTableVisitor.objects.filter(
                    tavern_table=self,
                    access=TavernTableVisitor.ACCESS_CODE_MAP[privilege],
                ).exclude(user_profile_id__in=all_affected_users).update(
                    access=TavernTableVisitor.ACCESS_CODE_MAP[
                        TavernAccessRights.DEFAULT
                    ]
                )
            elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                TavernTableVisitor.objects.filter(tavern_table=self, access=1).exclude(
                    user_profile_id__in=all_affected_users
                ).update(moderator=0)
            else:
                raise ValueError(f"Encountered unknown privilege {privilege}")

        # Next, reflect updated and added privileges
        for privilege in access_map:
            for user_id in access_map[privilege]:
                # Update to the user with either existing privileges or at least a tavern table visit
                if user_id in visitors_map:
                    visitor = visitors_map[user_id]

                    if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                        visitor.access = visitor.ACCESS_CODE_MAP[privilege]
                    elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                        visitor.moderator = 1

                    visitor.save()
                else:
                    args = {
                        "tavern_table": self,
                        "user_profile_id": user_id,
                    }
                    if privilege in TavernTableVisitor.ACCESS_CODE_MAP:
                        args["access"] = TavernTableVisitor.ACCESS_CODE_MAP[privilege]
                    elif privilege == TavernAccessRights.ASSISTANT_ADMIN:
                        args["moderator"] = 1

                    visitor = TavernTableVisitor.objects.create(**args)
                    # for handling situations like access allowed *and* assistant admin
                    visitors.append(visitor)
                    visitors_map[user_id] = visitor


class TavernBookmark(models.Model):
    tavern_table = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, db_column="id_uz"
    )
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_book"
        unique_together = (("tavern_table", "user_profile"),)


class TavernTableLink(models.Model):
    tavern_table_id = models.IntegerField(primary_key=True, db_column="id_stolu")
    linked_table_id = models.IntegerField(db_column="id_linku")

    class Meta:
        db_table = "putyka_linky"
        unique_together = (("tavern_table_id", "linked_table_id"),)


class TavernTableNoticeBoard(models.Model):
    tavern_table = models.OneToOneField(
        db_column="id_stolu", to=TavernTable, on_delete=models.CASCADE, primary_key=True
    )
    # TODO: Drop
    table_name = MisencodedCharField(max_length=128, db_column="nazev_stolu")
    text = MisencodedTextField(db_column="text_nastenky")
    changed_at = models.DateTimeField(blank=True, null=True, db_column="posledni_zmena")
    change_author_nick = MisencodedCharField(max_length=25, db_column="zmenil")

    class Meta:
        db_table = "putyka_nastenky"


class TavernPost(models.Model):
    tavern_table = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    text = MisencodedTextField(db_column="text")
    reputation = models.IntegerField(db_column="reputace")
    date = models.DateTimeField(db_column="datum")
    author_nick = MisencodedCharField(max_length=30, db_column="autor")
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True
    )

    # Comment template compatibility
    @property
    def nickname(self):
        return self.author_nick

    class Meta:
        db_table = "putyka_prispevky"


class TavernSection(models.Model):
    code = models.IntegerField(db_column="kod")
    order = models.IntegerField(db_column="poradi")
    name = MisencodedCharField(max_length=50, db_column="nazev")
    description = MisencodedCharField(max_length=255, db_column="popis")

    class Meta:
        db_table = "putyka_sekce"


class TavernTableVisitor(models.Model):
    """Tracking visits to a tavern table as well as bookmark status"""

    # TODO: Migrate to "table" and "user" attributes
    # :thinking: Shouldn't be too hard given we can leave the db_column in...
    tavern_table = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, db_column="id_uz"
    )
    # 1: Tavern Table is bookmarked
    # 0: Tavern Table is not bookmarked, but this record is used for visit keeping
    # -1: Tavern Table is ignored and should not be displayed
    favorite = models.IntegerField(default=0, db_column="oblibenost")
    visit_time = models.DateTimeField(blank=True, null=True, db_column="navstiveno")
    unread = models.IntegerField(blank=True, null=True, db_column="neprectenych")
    # Boolean: 1 means user is an assistent admin
    moderator = models.IntegerField(default=0, db_column="sprava")
    # 2 = Allow write
    # 1 = Allow access
    # 0 = Behave as normal user
    # -2 = Deny access
    access = models.IntegerField(default=0, db_column="pristup")
    django_id = models.AutoField(primary_key=True)

    ACCESS_CODE_MAP = {
        TavernAccessRights.ACCESS_ALLOWED: 1,
        TavernAccessRights.ACCESS_BANNED: -2,
        TavernAccessRights.WRITE_ALLOWED: 2,
        TavernAccessRights.DEFAULT: 0,
    }

    class Meta:
        db_table = "putyka_uzivatele"
        unique_together = (("tavern_table", "user_profile"),)


###
# Deprecated Features
###
class TavernTableMerge(models.Model):
    requestor_id = models.IntegerField(db_column="id_ja")
    merger_id = models.IntegerField(db_column="id_on")
    staying = models.SmallIntegerField(db_column="zustavam")
    marker = MisencodedCharField(max_length=60, db_column="oznaceni")

    class Meta:
        db_table = "putyka_slucovani"


class TavernVisit(models.Model):
    time = models.DateTimeField(primary_key=True, db_column="cas")
    place = MisencodedCharField(max_length=31, db_column="misto")
    number = models.IntegerField(db_column="pocet")

    class Meta:
        db_table = "putyka_navstevnost"
        unique_together = (("time", "place"),)


class IgnoredTavernTable(models.Model):
    user_profile_id = models.IntegerField(db_column="id_uz")
    tavern_table_id = models.IntegerField(db_column="id_stolu")

    class Meta:
        managed = False
        db_table = "putyka_neoblibene"


class TavernAccess(models.Model):
    """Tavern access was used in v0. Now it's preferred to store it as attributes in TavernTableVisitor"""

    tavern_table = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    # typ_pristupu is essentially an enum:
    # vstpo = Allow access even if otherwise denied
    # vstza = Deny access even if otherwise allowed
    # asist = Assistent admin, allow access even if otherwise denied
    # zapis = Allow write access even if table is read only
    access_type = MisencodedCharField(max_length=5, db_column="typ_pristupu")
    user_nick = MisencodedCharField(max_length=30, db_column="nick_usera")
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_pristup"
        unique_together = (("tavern_table", "access_type", "user_nick"),)
