# Generated by Django 2.0.13 on 2021-04-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0064_prefill_ids"),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE `mentat_newbie` DROP PRIMARY KEY;"),
        # This migration is skipped given the command above reconciles different ideas about
        # what primary key is between Django and MySQL
        # migrations.AlterField(
        #     model_name="mentatnewbie",
        #     name="newbie_id",
        #     field=models.IntegerField(),
        # ),
    ]