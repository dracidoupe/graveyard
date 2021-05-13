from datetime import datetime
from dateutil import tz
import logging
import sys

from ddcz.models import (
    TavernAccess,
    TavernTable,
    TavernTableVisitor,
    UserProfile,
    TAVERN_SECTION_PRIVATE_ID,
    TAVERN_SECTION_NEW_ID,
)
from ddcz.text import misencode

logger = logging.getLogger(__name__)


def get_tables_with_access(user_profile, candidate_tables_queryset):
    """Return tables from given queryset to which the user_profile has access to"""
    # This should be more optimized once we refactor the ACL model into a single row bit
    # See https://github.com/dracidoupe/graveyard/issues/233

    related_permissions = TavernAccess.objects.filter(
        nick_usera=misencode(user_profile.nick_uzivatele),
        id_stolu__in=[i.pk for i in candidate_tables_queryset],
    )

    related_permissions_map = {}

    for perm in related_permissions:
        if perm.id_stolu not in related_permissions_map:
            related_permissions_map[perm.id_stolu] = set()
        related_permissions_map[perm.id_stolu].add(perm.typ_pristupu)

    return [
        table
        for table in candidate_tables_queryset
        if table.is_user_access_allowed(
            user_profile,
            acls=related_permissions_map.get(table.pk, set()),
        )
    ]


def create_tavern_table(
    owner: UserProfile,
    name: str,
    description: str,
    public: bool = False,
    allow_reputation: bool = False,
) -> TavernTable:
    if public:
        section = TAVERN_SECTION_NEW_ID
        public_db = "1"
    else:
        section = TAVERN_SECTION_PRIVATE_ID
        public_db = "0"

    return TavernTable.objects.create(
        jmeno=name,
        popis=description,
        vlastnik=owner.nick_uzivatele,
        verejny=public_db,
        povol_hodnoceni="1" if allow_reputation else "0",
        # TODO: Those should go to model defaults
        sekce=section,
        zalozen=datetime.now(tz.gettz("Europe/Prague")),
    )


def migrate_tavern_access(
    print_progress=True,
    table_visitor_model=None,
    tavern_access_model=None,
    user_profile_model=None,
):
    """Migrate access privileges from putyka v0 (the DDCZ 2001 version) to putyka v1 (DDCZ 2004 version)"""

    i = 0

    if not table_visitor_model:
        table_visitor_model = TavernTableVisitor

    if not tavern_access_model:
        tavern_access_model = TavernAccess

    if not user_profile_model:
        user_profile_model = UserProfile

    # Completely accidentally, the `-typ_pristupu` gives us correct enough
    # ordering of access priorities
    for tavern_access in (
        tavern_access_model.objects.all()
        .select_related("id_stolu")
        .order_by("-typ_pristupu")
    ):
        if print_progress and i % 100 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()

        try:
            profile_id = user_profile_model.objects.get(
                nick_uzivatele=misencode(tavern_access.nick_usera)
            )
        except user_profile_model.DoesNotExist:
            # OK, this opens up a potential security problem, but so far, we don't have
            # Users with nick that would be composed of numbers only.
            # So let's try: sometimes, there is an integer in nick_usera that looks like
            # corresponding to a user ID, so let's use that for a secondary search
            try:
                profile_id = user_profile_model.objects.get(
                    id=int(tavern_access.nick_usera)
                )
            except (ValueError, user_profile_model.DoesNotExist):
                # OK, _now_ we give up
                logging.warn(
                    f"Can't fetch user record for nick {tavern_access.nick_usera}. Maybe we should purge the record?"
                )
        else:
            try:
                table_visitor = table_visitor_model.objects.get(
                    id_stolu=tavern_access.id_stolu, id_uzivatele=profile_id
                )
            except table_visitor_model.DoesNotExist:
                table_visitor = table_visitor_model(
                    id_stolu=tavern_access.id_stolu, id_uzivatele=profile_id
                )

            if tavern_access.typ_pristupu == "vstpo":
                table_visitor.pristup = 1
            elif tavern_access.typ_pristupu == "vstza":
                table_visitor.pristup = -2
            elif tavern_access.typ_pristupu == "zapis":
                table_visitor.pristup = 2
            elif tavern_access.typ_pristupu == "asist":
                table_visitor.sprava = 1
            else:
                logger.warn(
                    f"Unknown access type {tavern_access.typ_pristupu} for user {tavern_access.nick_usera} to table {tavern_access.id_stolu}"
                )

            table_visitor.save()

        i += 1
