# Generated by Django 2.0.13 on 2020-10-14 16:13

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0034_ranger_spell_rename"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="kouzla",
            options={},
        ),
        migrations.AddField(
            model_name="kouzla",
            name="precteno",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="autmail",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="autor",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="datum",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="dosahpop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="jmeno",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="kouzsl",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="magpop",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="past",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="pochvez",
            field=ddcz.models.magic.MisencodedIntegerField(max_length=5),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="popis",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="rozsahpop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="schvaleno",
            field=ddcz.models.magic.MisencodedCharField(
                choices=[("a", "Schváleno"), ("n", "Neschváleno")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="skupina",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="tisknuto",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="trvanipop",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="vyvolanipop",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="zdroj",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="kouzla",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
    ]
