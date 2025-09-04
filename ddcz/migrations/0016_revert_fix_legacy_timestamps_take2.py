import logging

from django.conf import settings
from django.db import migrations, transaction

logger = logging.getLogger(__name__)

# Re-run of the revert with type-aware cutoff handling and rowcount logging

MODEL_FIELDS = [
    ("ddcz", "Phorum", "date"),
    ("ddcz", "CreationComment", "date"),
    ("ddcz", "Letter", "date"),
    ("ddcz", "TavernTable", "created"),
    ("ddcz", "TavernTableNoticeBoard", "changed_at"),
    ("ddcz", "TavernPost", "date"),
    ("ddcz", "TavernTableVisitor", "visit_time"),
    ("ddcz", "TavernVisit", "time"),
    ("ddcz", "UserProfile", "last_login"),
    ("ddcz", "UserProfile", "registration_approved_date"),
    # Creations and related
    ("ddcz", "CommonArticle", "published"),
    ("ddcz", "Monster", "published"),
    ("ddcz", "GalleryPicture", "published"),
    ("ddcz", "Photo", "published"),
    ("ddcz", "Skill", "published"),
    ("ddcz", "AlchemistTool", "published"),
    ("ddcz", "RangerSpell", "published"),
    ("ddcz", "WizardSpell", "published"),
    ("ddcz", "Item", "published"),
    ("ddcz", "DownloadItem", "published"),
    ("ddcz", "Quest", "published"),
    ("ddcz", "Link", "published"),
    # Info / Social
    ("ddcz", "News", "date"),
    ("ddcz", "Dating", "published"),
    ("ddcz", "Market", "created"),
    # Notifications
    ("ddcz", "ScheduledNotification", "scheduled_at"),
    ("ddcz", "ScheduledEmail", "scheduled_at"),
]

SQL_TEMPLATE_REVERT_TSTZ = (
    "UPDATE {table} "
    "SET {col} = ({col} AT TIME ZONE %s) AT TIME ZONE 'UTC' "
    "WHERE {col} IS NOT NULL AND {col} < (TIMESTAMP %s AT TIME ZONE %s);"
)


def forwards(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    qn = connection.ops.quote_name

    tz_name = getattr(settings, "TIME_ZONE", "Europe/Prague")
    cutoff_local_str = "2025-09-03 04:00:00"  # local wall time

    table_columns = []
    for app_label, model_name, field_name in MODEL_FIELDS:
        try:
            Model = apps.get_model(app_label, model_name)
            field = Model._meta.get_field(field_name)
            col = field.db_column or field.column
            table = Model._meta.db_table
            table_columns.append((table, col))
        except Exception as e:
            logger.error(
                f"Error getting model {app_label}.{model_name} field {field_name}: {e}"
            )

    for table, col in table_columns:
        try:
            cursor.execute(
                """
                SELECT c.data_type
                FROM information_schema.columns c
                WHERE c.table_schema = current_schema()
                  AND c.table_name = %s
                  AND c.column_name = %s
                  AND c.data_type IN ('timestamp without time zone','timestamp with time zone')
                """,
                [table, col],
            )
            row = cursor.fetchone()
            if row is None:
                continue
            data_type = row[0]
        except Exception as e:
            logger.error(f"Error getting table {table} column {col}: {e}")
            continue

        if data_type == "timestamp without time zone":
            sql = (
                f"UPDATE {qn(table)} SET {qn(col)} = ({qn(col)} AT TIME ZONE %s) AT TIME ZONE 'UTC' "
                f"WHERE {qn(col)} IS NOT NULL AND {qn(col)} < TIMESTAMP %s;"
            )
            params = [tz_name, cutoff_local_str]
        else:
            sql = SQL_TEMPLATE_REVERT_TSTZ.format(table=qn(table), col=qn(col))
            params = [tz_name, cutoff_local_str, tz_name]

        try:
            with transaction.atomic(using=connection.alias):
                cursor.execute(sql, params)
                logger.info(
                    "Re-run revert for %s.%s (%s), rows affected: %s",
                    table,
                    col,
                    data_type,
                    cursor.rowcount,
                )
        except Exception as e:
            logger.error(f"Re-run revert failed for {table}.{col}: {e}")


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0015_revert_fix_legacy_timestamps"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
