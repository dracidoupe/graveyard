# Generated by Django 3.1.14 on 2025-01-16 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0010_dating_20241230_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dating',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_column='datum', null=True, verbose_name='Datum'),
        ),
    ]
