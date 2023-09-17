# Generated by Django 2.0.13 on 2021-07-19 16:21

import ddcz.models.magic
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0094_access_nick_or_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taverntable",
            name="allow_rep",
            field=ddcz.models.magic.MisencodedBooleanField(
                db_column="povol_hodnoceni", max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="taverntable",
            name="public",
            field=ddcz.models.magic.MisencodedBooleanField(
                db_column="verejny", max_length=1
            ),
        ),
    ]
