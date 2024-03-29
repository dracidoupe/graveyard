# Generated by Django 2.0.13 on 2020-10-16 16:14

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0038_item_rename"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="precteno",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="item",
            name="delka",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=3, null=True
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="kz",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, db_column="KZ", max_length=3, null=True
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="popis",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="item",
            name="skupina",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="item",
            name="uc",
            field=ddcz.models.magic.MisencodedTextField(
                blank=True, db_column="UC", null=True
            ),
        ),
    ]
