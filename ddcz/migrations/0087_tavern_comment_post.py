# Generated by Django 2.0.13 on 2021-06-12 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0086_renames_followup"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TavernComment",
            new_name="TavernPost",
        ),
        migrations.RenameField(
            model_name="tavernpost",
            old_name="tavern_table_id",
            new_name="tavern_table",
        ),
        migrations.RenameField(
            model_name="tavernpost",
            old_name="datum",
            new_name="date",
        ),
    ]
