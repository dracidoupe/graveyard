# Generated by Django 2.0.13 on 2020-03-04 14:54

import ddcz.models.magic
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0022_fix_levelsysparams"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dovednosti",
            options={},
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="autmail",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="autor",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="datum",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="fatneuspech",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="hlasoval",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="jmeno",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="neuspech",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="obtiznost",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="overovani",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="pochvez",
            field=ddcz.models.magic.MisencodedIntegerField(max_length=5),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="popis",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="precteno",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="schvaleno",
            field=ddcz.models.magic.MisencodedCharField(
                choices=[("a", "Schváleno"), ("n", "Neschváleno")], max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="skupina",
            field=ddcz.models.magic.MisencodedCharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="tisknuto",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="totuspech",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="uspech",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="vlastnost",
            field=ddcz.models.magic.MisencodedTextField(),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="zdroj",
            field=ddcz.models.magic.MisencodedTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="dovednosti",
            name="zdrojmail",
            field=ddcz.models.magic.MisencodedCharField(
                blank=True, max_length=30, null=True
            ),
        ),
    ]
