import logging

from django.db import migrations

from ddcz.creations import transfer_creations
from ddcz.text import misencode

logger = logging.getLogger(__name__)

SOURCE_PROFILE_ID = 15763  # Břečťan
TARGET_PROFILE_ID = 254  # Zombie

TRANSFERRED_CREATIONS = {
    "CommonArticle": [4260],  # Nešikovnost, rubrika zlodej
    "AlchemistTool": [628, 629],  # Štíří jícha, Bronzový popel
}

# Recreated on reverse at its original pk. `user_nick` is restored to the
# mangled value `manage.py migrateauthors` originally wrote, not a corrected
# one -- this predates the transfer and isn't this migration's to fix.
SOURCE_AUTHOR_ID = 3168
SOURCE_AUTHOR_USER_NICK = "B?e??an"

# statistiky_autori is keyed (autor, rubrika): forwards adds these counts
# into the target's existing rows, backwards subtracts them back out.
SOURCE_AUTHOR_STATS = (("alchpredmety", 2), ("zlodej", 1))

# statistiky_dila has no usable key; these `datum` values are unique across
# the whole table, so they identify the moved rows again on reverse.
SOURCE_WORK_STATS_DATES = (
    "2009-05-23 19:25:17+02",
    "2009-05-24 13:02:10+02",
    "2009-05-25 11:44:55+02",
)


def _table_exists(cursor, table_name):
    cursor.execute("SELECT to_regclass(%s)", [table_name])
    return cursor.fetchone()[0] is not None


def _move_author_stats(schema_editor, source_nick, target_nick):
    source = misencode(source_nick)
    target = misencode(target_nick)

    with schema_editor.connection.cursor() as cursor:
        if _table_exists(cursor, "statistiky_autori"):
            cursor.execute(
                """
                INSERT INTO statistiky_autori (autor, rubrika, pocet)
                SELECT %(target)s, rubrika, pocet
                FROM statistiky_autori WHERE autor = %(source)s
                ON CONFLICT (autor, rubrika) DO UPDATE
                    SET pocet = statistiky_autori.pocet + EXCLUDED.pocet
                """,
                {"source": source, "target": target},
            )
            cursor.execute(
                "DELETE FROM statistiky_autori WHERE autor = %(source)s",
                {"source": source},
            )

        if _table_exists(cursor, "statistiky_dila"):
            cursor.execute(
                "UPDATE statistiky_dila SET autor = %(target)s WHERE autor = %(source)s",
                {"source": source, "target": target},
            )
            if cursor.rowcount != len(SOURCE_WORK_STATS_DATES):
                logger.warning(
                    "statistiky_dila: expected to move %s rows for %r, moved %s -- "
                    "this table has no writer anywhere and is already stale, continuing",
                    len(SOURCE_WORK_STATS_DATES),
                    source_nick,
                    cursor.rowcount,
                )


def _restore_author_stats(schema_editor, source_nick, target_nick):
    source = misencode(source_nick)
    target = misencode(target_nick)

    with schema_editor.connection.cursor() as cursor:
        if _table_exists(cursor, "statistiky_autori"):
            for rubrika, pocet in SOURCE_AUTHOR_STATS:
                cursor.execute(
                    """
                    UPDATE statistiky_autori SET pocet = pocet - %(pocet)s
                     WHERE autor = %(target)s AND rubrika = %(rubrika)s
                    """,
                    {"target": target, "rubrika": rubrika, "pocet": pocet},
                )
                cursor.execute(
                    """
                    DELETE FROM statistiky_autori
                     WHERE autor = %(target)s AND rubrika = %(rubrika)s AND pocet <= 0
                    """,
                    {"target": target, "rubrika": rubrika},
                )
                cursor.execute(
                    """
                    INSERT INTO statistiky_autori (autor, rubrika, pocet)
                    VALUES (%(source)s, %(rubrika)s, %(pocet)s)
                    """,
                    {"source": source, "rubrika": rubrika, "pocet": pocet},
                )

        if _table_exists(cursor, "statistiky_dila"):
            cursor.execute(
                """
                UPDATE statistiky_dila SET autor = %(source)s
                 WHERE autor = %(target)s AND datum IN %(dates)s
                """,
                {
                    "source": source,
                    "target": target,
                    "dates": tuple(SOURCE_WORK_STATS_DATES),
                },
            )


def forwards(apps, schema_editor):
    Author = apps.get_model("ddcz", "Author")
    UserProfile = apps.get_model("ddcz", "UserProfile")

    if not Author.objects.filter(
        pk=SOURCE_AUTHOR_ID, user_id=SOURCE_PROFILE_ID
    ).exists():
        logger.info(
            "Author %s for profile %s already gone, assuming this migration "
            "already ran, skipping",
            SOURCE_AUTHOR_ID,
            SOURCE_PROFILE_ID,
        )
        return

    moved = transfer_creations(SOURCE_PROFILE_ID, TARGET_PROFILE_ID, apps=apps)
    if moved != TRANSFERRED_CREATIONS:
        raise RuntimeError(
            f"Expected to move {TRANSFERRED_CREATIONS}, actually moved {moved} -- "
            "production data has drifted since this migration was written, aborting "
            "rather than risk an incomplete or unreversible transfer"
        )

    source_nick = UserProfile.objects.get(pk=SOURCE_PROFILE_ID).nick
    target_nick = UserProfile.objects.get(pk=TARGET_PROFILE_ID).nick
    _move_author_stats(schema_editor, source_nick, target_nick)


def backwards(apps, schema_editor):
    Author = apps.get_model("ddcz", "Author")
    UserProfile = apps.get_model("ddcz", "UserProfile")

    if Author.objects.filter(pk=SOURCE_AUTHOR_ID).exists():
        logger.info(
            "Author %s already present, assuming this migration was already "
            "reversed, skipping",
            SOURCE_AUTHOR_ID,
        )
        return

    Author.objects.create(
        id=SOURCE_AUTHOR_ID,
        author_type="u",
        user_id=SOURCE_PROFILE_ID,
        user_nick=SOURCE_AUTHOR_USER_NICK,
    )

    transfer_creations(
        TARGET_PROFILE_ID,
        SOURCE_PROFILE_ID,
        apps=apps,
        creation_ids=TRANSFERRED_CREATIONS,
        delete_empty_source_author=False,
    )

    source_nick = UserProfile.objects.get(pk=SOURCE_PROFILE_ID).nick
    target_nick = UserProfile.objects.get(pk=TARGET_PROFILE_ID).nick
    _restore_author_stats(schema_editor, source_nick, target_nick)


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0022_fix_legacy_pk_sequences"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=backwards),
    ]
