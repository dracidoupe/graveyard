# Generated by Django 2.0.13 on 2023-09-17 17:10

import ddcz.models.magic
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0127_creation_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quest",
            name="abstract",
            field=ddcz.models.magic.MisencodedTextField(db_column="anotace"),
        ),
    ]
