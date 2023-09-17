# Generated by Django 2.0.13 on 2021-04-07 16:30

import ddcz.models.magic
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0053_auto_20210405_1623"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="diskuze",
            options={},
        ),
        migrations.AlterField(
            model_name="diskuze",
            name="cizi_tbl",
            field=ddcz.models.magic.MisencodedCharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="diskuze",
            name="email",
            field=ddcz.models.magic.MisencodedCharField(max_length=40),
        ),
        migrations.AlterField(
            model_name="diskuze",
            name="nickname",
            field=ddcz.models.magic.MisencodedCharField(max_length=25),
        ),
        migrations.AlterField(
            model_name="diskuze",
            name="text",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
    ]
