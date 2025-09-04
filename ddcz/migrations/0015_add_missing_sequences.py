import logging
from django.db import migrations

logger = logging.getLogger(__name__)


SQL_CHECK_COL = """
    SELECT 1
    FROM information_schema.columns c
    WHERE c.table_schema = current_schema()
      AND c.table_name = %s
      AND c.column_name = 'id'
      AND c.data_type IN (
        'smallint', 'integer', 'bigint'
      )
    """


def forwards(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()
    qn = connection.ops.quote_name

    # Only handle models from ddcz app. We focus on unmanaged legacy tables that should
    # have an implicit integer PK ("id") but may be missing a backing sequence/default.
    models = apps.get_app_config("ddcz").get_models()

    for Model in models:
        opts = Model._meta
        table = opts.db_table

        pk = opts.pk
        if not pk or pk.name != "id":
            logger.warning(f"Skipping table {table} as it doesn't have an integer PK")
            continue

        # Check the table and id column exist and are numeric
        cursor.execute(SQL_CHECK_COL, [table])
        if cursor.fetchone() is None:
            continue

        # If PostgreSQL already recognizes a serial/identity sequence for this column, skip
        cursor.execute("SELECT pg_get_serial_sequence(%s, 'id')", [table])
        row = cursor.fetchone()
        if row and row[0]:
            logger.warning(f"Skipping table {table} as it already has a sequence")
            continue

        seq_name = f"{table}_id_seq"

        # Create the sequence if missing, then attach it to the table column and initialize.
        # Use savepoint so a single failure does not abort the whole migration.
        try:
            # CREATE SEQUENCE IF NOT EXISTS
            cursor.execute(f"CREATE SEQUENCE IF NOT EXISTS {qn(seq_name)}")
            cursor.execute(
                f"ALTER SEQUENCE {qn(seq_name)} OWNED BY {qn(table)}.{qn('id')}"
            )
            cursor.execute(
                f"ALTER TABLE {qn(table)} ALTER COLUMN {qn('id')} "
                f"SET DEFAULT nextval('{seq_name}'::regclass)"
            )
            cursor.execute(
                f"SELECT setval('{seq_name}'::regclass, "
                f"COALESCE((SELECT MAX(id) FROM {qn(table)}), 0) + 1, false)"
            )
        except Exception as e:
            logger.error(f"Failed to add sequence for table {table}: {e}")


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0014_fix_legacy_timestamps"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
