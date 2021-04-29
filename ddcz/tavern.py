from ddcz.models.used.tavern import TavernAccess


def get_tables_with_access(user_profile, candidate_tables_queryset):
    """Return tables from given queryset to which the user_profile has access to"""
    # This should be more optimized once we refactor the ACL model into a single row bit
    # See https://github.com/dracidoupe/graveyard/issues/233

    related_permissions = TavernAccess.objects.filter(
        nick_usera=user_profile.nick_uzivatele,
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
