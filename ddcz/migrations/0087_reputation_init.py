# Generated by Django 2.0.13 on 2021-06-13 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0086_renames_followup"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reputacelog",
            options={},
        ),
        migrations.AlterModelOptions(
            name="reputacespecial",
            options={},
        ),
        migrations.RenameModel(
            old_name="ReputaceSpecial",
            new_name="ReputationAdditional",
        ),
        migrations.RenameModel(
            old_name="ReputaceLog",
            new_name="ReputationLog",
        ),
    ]
