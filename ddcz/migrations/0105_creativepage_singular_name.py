# Generated by Django 2.0.13 on 2021-08-15 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0104_runes_and_userrating_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='creativepage',
            name='singular_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]