# Generated by Django 2.0.13 on 2021-07-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0098_tavern_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reputationlog",
            name="discussion",
            field=models.CharField(
                blank=True, db_column="v_diskusi", max_length=1, null=True
            ),
        ),
    ]
