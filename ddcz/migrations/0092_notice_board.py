# Generated by Django 2.0.13 on 2021-06-28 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0091_tavern_post_nick"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                (
                    """
            ALTER TABLE
                `putyka_nastenky`
            ALTER COLUMN
                `posledni_zmena`
            SET DEFAULT NULL
            """
                )
            ],
            reverse_sql=[],
        ),
        migrations.AlterField(
            model_name="taverntablenoticeboard",
            name="tavern_table_id",
            field=models.OneToOneField(
                db_column="id_stolu",
                on_delete=django.db.models.deletion.CASCADE,
                to="ddcz.TavernTable",
            ),
        ),
        migrations.RenameField(
            model_name="taverntablenoticeboard",
            old_name="tavern_table_id",
            new_name="tavern_table",
        ),
        migrations.RenameField(
            model_name="taverntablenoticeboard",
            old_name="change_owner",
            new_name="change_author_nick",
        ),
        migrations.RenameField(
            model_name="taverntablenoticeboard",
            old_name="changed",
            new_name="changed_at",
        ),
    ]
