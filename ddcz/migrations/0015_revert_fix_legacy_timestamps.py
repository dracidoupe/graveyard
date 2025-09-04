import logging

from django.conf import settings
from django.db import migrations, transaction

logger = logging.getLogger(__name__)

# This migration reverts the mistaken timestamp reinterpretation done in 0014.
# Context: 0014 attempted to "fix" legacy timestamps before a cutoff, but this was only
# a local environment issue and should not have been applied in production. We now
# reverse the effect for rows before the same cutoff wall time.

# Define model fields to adjust (app_label, ModelName, field_name) — mirror 0014
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

# In 0014, we used:
#   SET col = (col AT TIME ZONE 'UTC') AT TIME ZONE %s
# for rows with:
#   col < (TIMESTAMP %s AT TIME ZONE %s)
#
# To revert, we invert the transformation:
#   SET col = (col AT TIME ZONE %s) AT TIME ZONE 'UTC'
# using the same cutoff condition.
SQL_TEMPLATE_REVERT = (
    "UPDATE {table} "
    "SET {col} = ({col} AT TIME ZONE %s) AT TIME ZONE 'UTC' "
    "WHERE {col} IS NOT NULL AND {col} < (TIMESTAMP %s AT TIME ZONE %s);"
)


def forwards(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    qn = connection.ops.quote_name

    tz_name = getattr(settings, "TIME_ZONE", "Europe/Prague")
    cutoff_local_str = "2025-09-03 04:00:00"  # local wall time in settings.TIME_ZONE

    # Resolve table/column names dynamically, mirroring 0014
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
        # Ensure column exists and is a timestamp type in current schema
        try:
            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns c
                WHERE c.table_schema = current_schema()
                  AND c.table_name = %s
                  AND c.column_name = %s
                  AND c.data_type IN ('timestamp without time zone','timestamp with time zone')
                """,
                [table, col],
            )
            if cursor.fetchone() is None:
                continue
        except Exception as e:
            logger.error(f"Error getting table {table} column {col}: {e}")
            continue

        sql = SQL_TEMPLATE_REVERT.format(table=qn(table), col=qn(col))
        try:
            with transaction.atomic(using=connection.alias):
                cursor.execute(sql, [tz_name, cutoff_local_str, tz_name])
        except Exception as e:
            logger.error(
                f"Reverting legacy timestamp fix failed for {table}.{col}: {e}"
            )


def backwards(apps, schema_editor):
    # Re-applying the mistaken change is not desired; make reverse a no-op.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0014_fix_legacy_timestamps"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
