from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0016_another_tz_migration"),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
            DO $$
            DECLARE
                tbl_regclass regclass := 'uzivatele_cekajici'::regclass;
                tbl_oid oid;
                tbl_schema text;
                seq_name text := 'uzivatele_cekajici_id_zaznamu_seq';
                fq_seq text;
                fq_tbl text;
            BEGIN
                -- Resolve table OID and schema
                SELECT c.oid, n.nspname INTO tbl_oid, tbl_schema
                FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE c.oid = tbl_regclass;

                IF tbl_oid IS NULL THEN
                    RAISE EXCEPTION 'Table uzivatele_cekajici not found';
                END IF;

                fq_seq := quote_ident(tbl_schema) || '.' || quote_ident(seq_name);
                fq_tbl := quote_ident(tbl_schema) || '.uzivatele_cekajici';

                -- Create the sequence in the same schema as the table if it does not exist there
                IF NOT EXISTS (
                    SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE c.relkind = 'S' AND c.relname = seq_name AND n.nspname = tbl_schema
                ) THEN
                    EXECUTE 'CREATE SEQUENCE ' || fq_seq;
                END IF;

                -- Initialize the sequence to max(id_zaznamu) or 1 if table is empty
                EXECUTE 'SELECT setval(''' || fq_seq || ''', COALESCE((SELECT MAX(id_zaznamu) FROM ' || fq_tbl || '), 1))';

                -- Ensure the column has a default from the sequence (schema-qualified)
                EXECUTE 'ALTER TABLE ' || fq_tbl || ' ALTER COLUMN id_zaznamu SET DEFAULT nextval(''' || fq_seq || '''::regclass)';

                -- Ensure ownership for cascade behavior (sequence and table must be in same schema)
                EXECUTE 'ALTER SEQUENCE ' || fq_seq || ' OWNED BY ' || fq_tbl || '.id_zaznamu';
            END
            $$;
            """,
            reverse_sql=r"""
            DO $$
            DECLARE
                tbl_regclass regclass := 'uzivatele_cekajici'::regclass;
                tbl_oid oid;
                tbl_schema text;
                fq_tbl text;
            BEGIN
                SELECT c.oid, n.nspname INTO tbl_oid, tbl_schema
                FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE c.oid = tbl_regclass;

                IF tbl_oid IS NULL THEN
                    -- Table not found; nothing to do
                    RETURN;
                END IF;

                fq_tbl := quote_ident(tbl_schema) || '.uzivatele_cekajici';
                EXECUTE 'ALTER TABLE ' || fq_tbl || ' ALTER COLUMN id_zaznamu DROP DEFAULT';
            END
            $$;
            """,
        ),
    ]
