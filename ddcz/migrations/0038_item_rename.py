# Generated by Django 2.0.13 on 2020-10-16 15:04

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0037_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Predmety',
            new_name='Item',
        ),
    ]
