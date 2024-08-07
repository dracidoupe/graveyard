from copy import deepcopy
from enum import Enum, unique
from itertools import chain

from django.db import models

from .users import UserProfile
from ..magic import MisencodedCharField, MisencodedTextField, MisencodedBooleanField
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
    allow_rep = MisencodedBooleanField(max_length=1, db_column="povol_hodnoceni")
    # TODO: Not used, to my knowledge; fine to drop the column, but double-check old code
    min_level = MisencodedCharField(max_length=1, db_column="min_level")
    created = models.DateTimeField(db_column="zalozen", auto_now_add=True)
    public = MisencodedBooleanField(max_length=1, db_column="verejny")
    posts_no = models.IntegerField(db_column="celkem", default=0)
    # TODO: FK migration
    section = models.IntegerField(db_column="sekce")

    @property
    def is_public(self):
        return self.public

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

        # Speedup cache for listing; see ddcz.tavern.get_tavern_table_list
        # TODO: Refactor and reconcile with elif below
        if getattr(self, "access_privileges_annotated", None):
            if self.is_assistant_admin:
                return True
            if self.is_banned:
                return False
            elif self.is_public:
                return True
            elif self.is_allowed:
                return True
            else:
                return False

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

    def is_admin(self, user_profile, acls=None):
        return user_profile.nick == self.owner

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
        # This is fucked up thanks to <https://github.com/dracidoupe/graveyard/issues/306>
        # Will be fixed by the permission model upgrade
        acls = [
            TavernAccessRights(acl.access_type)
            for acl in self.tavernaccess_set.filter(
                ~models.Q(access_type=TavernAccessRights.ASSISTANT_ADMIN),
                user_nick_or_id=misencode(user_profile.nick),
            )
        ]
        acls.extend(
            [
                TavernAccessRights(acl.access_type)
                for acl in self.tavernaccess_set.filter(
                    access_type=TavernAccessRights.ASSISTANT_ADMIN,
                    user_nick_or_id=user_profile.pk,
                )
            ]
        )
        return set(acls)

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
            unprocessed_access_map[TavernAccessRights.ASSISTANT_ADMIN] = set(
                assistant_admins
            )
            processing_privileges.add(TavernAccessRights.ASSISTANT_ADMIN)

        self.update_legacy_privileges(
            unprocessed_access_map=unprocessed_access_map,
            processing_privileges=processing_privileges,
        )
        self.update_future_privileges(
            unprocessed_access_map=unprocessed_access_map,
            processing_privileges=processing_privileges,
        )

    def get_current_privileges_map(self):
        """
        :return: current privileges as a dictionary in the format of
        {
            TavernAccessRights.RELEVANT_ENUM: set(['list', 'of', 'user', 'nicknames'])
        }

        This is format convenient for form mapping.
        """

        privileges = TavernAccess.objects.filter(tavern_table=self)
        privileges_map = {
            TavernAccessRights.ACCESS_ALLOWED: set([]),
            TavernAccessRights.WRITE_ALLOWED: set([]),
            TavernAccessRights.ACCESS_BANNED: set([]),
            TavernAccessRights.ASSISTANT_ADMIN: set([]),
        }

        for privilege in privileges:
            access_type = TavernAccessRights(privilege.access_type)
            if access_type == TavernAccessRights.ASSISTANT_ADMIN and isinstance(
                privilege.user_nick_or_id, int
            ):
                nick = UserProfile.objects.values("nick").get(
                    pk=privilege.user_nick_or_id
                )["nick"]
            else:
                nick = privilege.user_nick_or_id

            privileges_map[access_type].add(nick)

        return privileges_map

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
        # Copy as we are using it as processing queue and it needs to be retained
        # for updating future privileges
        access_map = deepcopy(unprocessed_access_map)
        table_acls_to_delete = []
        table_acls_models = self.tavernaccess_set.filter(
            access_type__in=[p.value for p in processing_privileges]
        )
        # Diff in-database ACLs against the new set
        # Not in new set = delete from db; is in new set = leave untouched
        for acl in table_acls_models:
            access_type = TavernAccessRights(acl.access_type)
            if acl.pk not in access_map[access_type]:
                table_acls_to_delete.append(acl.pk)
            else:
                access_map[access_type].remove(acl.pk)

        # Adding new privileges
        for access_type in access_map:
            for user_id in access_map[access_type]:
                TavernAccess.objects.create(
                    tavern_table=self,
                    access_type=access_type.value,
                    user_nick_or_id=UserProfile.objects.get(pk=user_id).nick,
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

    @property
    def by_registered_user(self):
        return True

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
    """
    Tavern access was used in v0 and is the normativer version now.
     Once old version is shut down, it will be preferred to store
     it as attributes in TavernTableVisitor instead
    """

    tavern_table = models.ForeignKey(
        TavernTable, on_delete=models.CASCADE, db_column="id_stolu"
    )
    # typ_pristupu is essentially an enum:
    # vstpo = Allow access even if otherwise denied
    # vstza = Deny access even if otherwise allowed
    # asist = Assistent admin, allow access even if otherwise denied
    # zapis = Allow write access even if table is read only
    access_type = MisencodedCharField(max_length=5, db_column="typ_pristupu")
    # For everything except asist, it's user's nickname
    # for assist, it's ID
    # Burn it with fire, see <https://github.com/dracidoupe/graveyard/issues/306>
    user_nick_or_id = MisencodedCharField(max_length=30, db_column="nick_usera")
    django_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "putyka_pristup"
        unique_together = (("tavern_table", "access_type", "user_nick_or_id"),)

    def __str__(self):
        return f"PK {self.pk}: {self.access_type} for user {self.user_nick_or_id}"
