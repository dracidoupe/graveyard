# Generated by Django 2.0.13 on 2021-04-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0062_mentat"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentatnewbie",
            name="django_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
