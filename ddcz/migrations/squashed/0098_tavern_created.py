# Generated by Django 2.0.13 on 2021-07-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0097_posts_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taverntable",
            name="created",
            field=models.DateTimeField(auto_now_add=True, db_column="zalozen"),
        ),
    ]