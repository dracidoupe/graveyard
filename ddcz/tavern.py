import logging
import sys
from datetime import datetime

from dateutil import tz
from django.db.models import Count, OuterRef, Subquery, IntegerField

from ddcz.models import (
    TavernAccess,
    TavernTable,
    TavernTableVisitor,
    UserProfile,
    TAVERN_SECTION_PRIVATE_ID,
    TAVERN_SECTION_NEW_ID,
)
from ddcz.models.used.tavern import TavernBookmark
from ddcz.text import misencode

logger = logging.getLogger(__name__)

LIST_FAVORITE = "oblibene"
LIST_FAVORITE_NEW_COMMENTS = "oblibene_nove_komentare"
LIST_ALL = "vsechny"
LIST_ALL_NEW_COMMENTS = "vsechny_nove_komentare"

SUPPORTED_LIST_STYLES_DISPLAY_NAME = {
    LIST_FAVORITE: "Oblíbené",
    LIST_FAVORITE_NEW_COMMENTS: "Oblíbené s novými komentáři",
    LIST_ALL: "Všechny",
    LIST_ALL_NEW_COMMENTS: "Všechny s novými komentáři",
}


def get_tavern_table_list(user_profile, list_style):
    if list_style in [LIST_FAVORITE, LIST_FAVORITE_NEW_COMMENTS]:
        query = user_profile.tavern_bookmarks
    elif list_style in [LIST_ALL, LIST_ALL_NEW_COMMENTS]:
        query = TavernTable.objects.all()

    query = query.annotate(
        comments_no=Count(
            "tavernpost",
        ),
        # This should work, but it doesn't. Maybe bug in 2.0 and will be solved by upgrade?
        # Should cause LEFT OUTER JOIN putyka_uzivatele pu ON pu.id_uzivatele = $ID AND pu.id_stolu=putyka.id
        # visitor=FilteredRelation(
        #     "taverntablevisitor",
        #     condition=Q(taverntablevisitor__id_uzivatele=request.ddcz_profile.pk),
        # ),
        # # In lieu of that, solve it using subqueries
        new_comments_no=Subquery(
            TavernTableVisitor.objects.filter(
                tavern_table_id=OuterRef("id"), user_profile=user_profile
            ).values("unread")[:1],
            output_field=IntegerField(),
        ),
    ).order_by("name")

    if list_style in [LIST_ALL_NEW_COMMENTS, LIST_FAVORITE_NEW_COMMENTS]:
        query = query.filter(new_comments_no__gt=0)

    return list(query)


def get_tables_with_access(user_profile, candidate_tables_queryset):
    """
    DEPRECATED: Not used by listing, requirements changed. Keeping it around for potential API.
    Return tables from given queryset to which the user_profile has access to
    """
    # This should be more optimized once we refactor the ACL model into a single row bit
    # See https://github.com/dracidoupe/graveyard/issues/233

    related_permissions = TavernAccess.objects.filter(
        user_nick=misencode(user_profile.nick),
        tavern_table_id__in=[i.pk for i in candidate_tables_queryset],
    )

    related_permissions_map = {}

    for perm in related_permissions:
        if perm.tavern_table.pk not in related_permissions_map:
            related_permissions_map[perm.tavern_table.pk] = set()
        related_permissions_map[perm.tavern_table.pk].add(perm.access_type)

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
        name=name,
        description=description,
        owner=owner.nick,
        public=public_db,
        allow_rep="1" if allow_reputation else "0",
        # TODO: Those should go to model defaults
        section=section,
        created=datetime.now(tz.gettz("Europe/Prague")),
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
        .select_related("tavern_table")
        .order_by("-access_type")
    ):
        if print_progress and i % 100 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()

        try:
            user_profile = user_profile_model.objects.get(
                nick=misencode(tavern_access.user_nick)
            )
        except user_profile_model.DoesNotExist:
            # OK, this opens up a potential security problem, but so far, we don't have
            # Users with nick that would be composed of numbers only.
            # So let's try: sometimes, there is an integer in nick_usera that looks like
            # corresponding to a user ID, so let's use that for a secondary search
            try:
                user_profile = user_profile_model.objects.get(
                    id=int(tavern_access.user_nick)
                )
            except (ValueError, user_profile_model.DoesNotExist):
                # OK, _now_ we give up
                logging.warn(
                    f"Can't fetch user record for nick {tavern_access.user_nick}. Maybe we should purge the record?"
                )
        else:
            try:
                table_visitor = table_visitor_model.objects.get(
                    tavern_table=tavern_access.tavern_table, user_profile=user_profile
                )
            except table_visitor_model.DoesNotExist:
                table_visitor = table_visitor_model(
                    tavern_table=tavern_access.tavern_table, user_profile=user_profile
                )

            if tavern_access.access_type == "vstpo":
                table_visitor.access = 1
            elif tavern_access.access_type == "vstza":
                table_visitor.access = -2
            elif tavern_access.access_type == "zapis":
                table_visitor.access = 2
            elif tavern_access.access_type == "asist":
                table_visitor.moderator = 1
            else:
                logger.warn(
                    f"Unknown access type {tavern_access.access_type} for user {tavern_access.user_nick} to table {tavern_access.tavern_table}"
                )

            table_visitor.save()

        i += 1


def bookmark_table(user_profile, tavern_table):
    return TavernBookmark.objects.create(
        tavern_table=tavern_table, user_profile=user_profile
    )
