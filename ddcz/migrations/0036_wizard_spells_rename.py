# Generated by Django 2.0.13 on 2020-10-14 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0035_wizard_spells"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Kouzla",
            new_name="WizardSpell",
        ),
    ]
