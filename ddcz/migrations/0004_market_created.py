# Generated by Django 3.1.14 on 2024-12-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0003_plurals_20241229_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='created',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Přidáno'),
        ),
    ]
