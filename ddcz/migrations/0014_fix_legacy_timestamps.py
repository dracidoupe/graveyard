import logging

from django.conf import settings
from django.db import migrations, transaction

logger = logging.getLogger(__name__)


# Cutoff: 3. 9. 2025 4:00 Europe/Prague
# We will compute the corresponding UTC instant in SQL using AT TIME ZONE and compare against timestamptz values.

# Define model fields to adjust (app_label, ModelName, field_name)
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

# Note: The migration resolves actual DB table and column names at runtime via apps.get_model.


# We will compute cutoff in SQL: (timestamp %s AT TIME ZONE %s)
SQL_TEMPLATE = (
    "UPDATE {table} "
    "SET {col} = ({col} AT TIME ZONE 'UTC') AT TIME ZONE %s "
    "WHERE {col} IS NOT NULL AND {col} < (TIMESTAMP %s AT TIME ZONE %s);"
)


def forwards(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    qn = connection.ops.quote_name

    tz_name = getattr(settings, "TIME_ZONE", "Europe/Prague")
    cutoff_local_str = "2025-09-03 04:00:00"  # local wall time in settings.TIME_ZONE

    # Build table/column list dynamically from models to avoid stale names
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
        # Skip if table doesn't exist or column missing
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

        sql = SQL_TEMPLATE.format(table=qn(table), col=qn(col))
        try:
            # Execute inside a savepoint to avoid aborting the whole migration on a single failure
            with transaction.atomic(using=connection.alias):
                cursor.execute(sql, [tz_name, cutoff_local_str, tz_name])
        except Exception as e:
            # Best-effort: log and continue
            logger.error(f"Legacy timestamp fix failed for {table}.{col}: {e}")


def backwards(apps, schema_editor):
    # Irreversible: we cannot know which rows were corrected vs originally correct without
    # additional markers. Provide a no-op reverse migration.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0013_auto_20250903_0005"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
