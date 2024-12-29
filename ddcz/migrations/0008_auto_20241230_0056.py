# Generated by Django 3.1.14 on 2024-12-29 23:56

import ddcz.models.magic
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0007_nonnull_20241229_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ddcz.userprofile'),
        ),
        migrations.AlterField(
            model_name='market',
            name='area',
            field=ddcz.models.magic.MisencodedCharField(blank=True, db_column='okres', max_length=20, null=True, verbose_name='Kraj'),
        ),
        migrations.AlterField(
            model_name='market',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Přidáno'),
        ),
        migrations.AlterField(
            model_name='market',
            name='mail',
            field=ddcz.models.magic.MisencodedCharField(blank=True, db_column='mail', max_length=50, null=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='market',
            name='name',
            field=ddcz.models.magic.MisencodedCharField(blank=True, db_column='jmeno', max_length=100, null=True, verbose_name='Jméno'),
        ),
    ]
