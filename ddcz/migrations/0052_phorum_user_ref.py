# Generated by Django 2.0.13 on 2020-11-20 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddcz', '0051_author_cache_nick'),
    ]

    operations = [
        migrations.AddField(
            model_name='phorum',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ddcz.UserProfile'),
        ),
    ]
