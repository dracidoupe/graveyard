# Generated by Django 2.0.2 on 2018-06-13 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ddcz", "0009_auto_20180610_2246"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreativePage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("slug", models.SlugField(max_length=30)),
                ("model_class", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="CreativePageConcept",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "page",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ddcz.CreativePage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CreativePageSection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("slug", models.SlugField(max_length=30)),
            ],
        ),
    ]
