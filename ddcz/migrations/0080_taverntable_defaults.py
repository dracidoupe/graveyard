# Generated by Django 2.0.13 on 2021-05-05 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0079_tavernvisitor_fk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taverntablevisitor",
            name="oblibenost",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="taverntablevisitor",
            name="pristup",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="taverntablevisitor",
            name="sprava",
            field=models.IntegerField(default=0),
        ),
    ]
