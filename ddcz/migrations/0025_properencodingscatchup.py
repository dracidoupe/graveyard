# Generated by Django 2.0.13 on 2020-10-10 16:05

import ddcz.models.magic
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0024_skills_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commonarticle",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="gallerypicture",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="monster",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="photo",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="skill",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
    ]
