from django.db import migrations

# Add FKs missed during pgloader shenanigans
LEGACY_DJANGO_ID_TABLES = [
    "putyka_book",
    "putyka_uzivatele",
    "putyka_pristup",
    "mentat_newbie",
    "hlasovani_prispevky",
    "uzivatele_maillist",
]

_TABLE_ARRAY_SQL = "ARRAY[{}]".format(
    ",\n                    ".join(f"'{table}'" for table in LEGACY_DJANGO_ID_TABLES)
)


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0021_alter_userprofile_tavern_bookmarks"),
    ]

    operations = [
        migrations.RunSQL(
            sql=rf"""
            DO $$
            DECLARE
                tbl_name text;
                tbl_names text[] := {_TABLE_ARRAY_SQL};
                tbl_regclass regclass;
                tbl_oid oid;
                tbl_schema text;
                seq_name text;
                fq_seq text;
                fq_tbl text;
            BEGIN
                FOREACH tbl_name IN ARRAY tbl_names LOOP
                    BEGIN
                        tbl_regclass := tbl_name::regclass;
                    EXCEPTION WHEN undefined_table THEN
                        CONTINUE;
                    END;

                    SELECT c.oid, n.nspname INTO tbl_oid, tbl_schema
                    FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE c.oid = tbl_regclass;

                    -- On databases created fresh under Django 4.1+, django_id is an
                    -- identity column: it already auto-increments and SET DEFAULT
                    -- would fail. The sequence fix is only needed for the legacy
                    -- pgloader import.
                    IF EXISTS (
                        SELECT 1 FROM pg_attribute
                        WHERE attrelid = tbl_oid AND attname = 'django_id' AND attidentity <> ''
                    ) THEN
                        CONTINUE;
                    END IF;

                    -- Already has a default (already fixed, or otherwise healthy) - no-op.
                    IF EXISTS (
                        SELECT 1 FROM pg_attribute
                        WHERE attrelid = tbl_oid AND attname = 'django_id' AND atthasdef
                    ) THEN
                        CONTINUE;
                    END IF;

                    seq_name := tbl_name || '_django_id_seq';
                    fq_seq := quote_ident(tbl_schema) || '.' || quote_ident(seq_name);
                    fq_tbl := quote_ident(tbl_schema) || '.' || quote_ident(tbl_name);

                    -- Create the sequence in the same schema as the table if it does not exist there
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                        WHERE c.relkind = 'S' AND c.relname = seq_name AND n.nspname = tbl_schema
                    ) THEN
                        EXECUTE 'CREATE SEQUENCE ' || fq_seq;
                    END IF;

                    -- Initialize the sequence to max(django_id) or 1 if table is empty
                    EXECUTE 'SELECT setval(''' || fq_seq || ''', COALESCE((SELECT MAX(django_id) FROM ' || fq_tbl || '), 1))';

                    -- Ensure the column has a default from the sequence (schema-qualified)
                    EXECUTE 'ALTER TABLE ' || fq_tbl || ' ALTER COLUMN django_id SET DEFAULT nextval(''' || fq_seq || '''::regclass)';

                    -- Ensure ownership for cascade behavior (sequence and table must be in same schema)
                    EXECUTE 'ALTER SEQUENCE ' || fq_seq || ' OWNED BY ' || fq_tbl || '.django_id';
                END LOOP;
            END
            $$;
            """,
            reverse_sql=rf"""
            DO $$
            DECLARE
                tbl_name text;
                tbl_names text[] := {_TABLE_ARRAY_SQL};
                tbl_regclass regclass;
                tbl_oid oid;
                tbl_schema text;
                fq_tbl text;
            BEGIN
                FOREACH tbl_name IN ARRAY tbl_names LOOP
                    BEGIN
                        tbl_regclass := tbl_name::regclass;
                    EXCEPTION WHEN undefined_table THEN
                        CONTINUE;
                    END;

                    SELECT c.oid, n.nspname INTO tbl_oid, tbl_schema
                    FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE c.oid = tbl_regclass;

                    -- Identity columns (Django 4.1+ fresh databases) have no default to drop
                    IF EXISTS (
                        SELECT 1 FROM pg_attribute
                        WHERE attrelid = tbl_oid AND attname = 'django_id' AND attidentity <> ''
                    ) THEN
                        CONTINUE;
                    END IF;

                    fq_tbl := quote_ident(tbl_schema) || '.' || quote_ident(tbl_name);
                    EXECUTE 'ALTER TABLE ' || fq_tbl || ' ALTER COLUMN django_id DROP DEFAULT';
                END LOOP;
            END
            $$;
            """,
        ),
    ]
