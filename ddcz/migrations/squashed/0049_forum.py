# Generated by Django 2.0.13 on 2020-11-17 16:27

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0048_author_squashed_0050_author_anonymous"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="forum",
            options={},
        ),
        migrations.AlterField(
            model_name="forum",
            name="datum",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="forum",
            name="email",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="forum",
            name="nickname",
            field=ddcz.models.magic.MisencodedCharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="forum",
            name="reg",
            field=ddcz.models.magic.MisencodedCharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="forum",
            name="text",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
    ]
