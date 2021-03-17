# Generated by Django 2.0.13 on 2020-10-14 15:48

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0032_links_approval"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="hranicarkouzla",
            options={},
        ),
        migrations.AddField(
            model_name="hranicarkouzla",
            name="precteno",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="autmail",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="autor",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="cetnost",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="datum",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="dosahpop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="druh",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="jmeno",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="magpop",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="pochvez",
            field=ddcz.models.magic.MisencodedIntegerField(max_length=5),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="pomucky",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="popis",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="rozsahpop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="schvaleno",
            field=ddcz.models.magic.MisencodedCharField(
                choices=[("a", "Schváleno"), ("n", "Neschváleno")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="skupina",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="tisknuto",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="vyvolanipop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="zdroj",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hranicarkouzla",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
    ]
