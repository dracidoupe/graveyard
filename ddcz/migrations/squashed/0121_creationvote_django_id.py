# Generated by Django 2.0.13 on 2022-01-09 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0120_votes_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="creationvote",
            name="django_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
