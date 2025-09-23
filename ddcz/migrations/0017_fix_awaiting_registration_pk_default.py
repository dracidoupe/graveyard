from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0016_another_tz_migration"),
    ]

    operations = [
        migrations.RunSQL(
            sql=r"""
            DO $$
            BEGIN
                -- Create the sequence if it does not exist
                IF NOT EXISTS (
                    SELECT 1 FROM pg_class WHERE relname = 'uzivatele_cekajici_id_zaznamu_seq'
                ) THEN
                    CREATE SEQUENCE uzivatele_cekajici_id_zaznamu_seq;

                    -- Initialize the sequence to max(id_zaznamu) or 1 if table is empty
                    PERFORM setval(
                        'uzivatele_cekajici_id_zaznamu_seq',
                        COALESCE((SELECT MAX(id_zaznamu) FROM uzivatele_cekajici), 1)
                    );
                END IF;

                -- Ensure the column has a default from the sequence
                EXECUTE 'ALTER TABLE uzivatele_cekajici ALTER COLUMN id_zaznamu SET DEFAULT nextval('''
                        || 'uzivatele_cekajici_id_zaznamu_seq' || '''::regclass)';

                -- Ensure ownership for cascade behavior
                EXECUTE 'ALTER SEQUENCE uzivatele_cekajici_id_zaznamu_seq OWNED BY uzivatele_cekajici.id_zaznamu';
            END
            $$;
            """,
            reverse_sql=r"""
            -- Revert to no default; keep sequence intact to avoid data loss
            ALTER TABLE uzivatele_cekajici ALTER COLUMN id_zaznamu DROP DEFAULT;
            """,
        ),
    ]
