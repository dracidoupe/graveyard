# Generated by Django 2.0.13 on 2021-08-08 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0101_remove_taverntablenoticeboard_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="posta",
            options={},
        ),
        migrations.AlterField(
            model_name="posta",
            name="datum",
            field=models.DateTimeField(db_column="datum"),
        ),
        migrations.AlterField(
            model_name="posta",
            name="odesilatel",
            field=models.CharField(db_column="odesilatel", max_length=25),
        ),
        migrations.AlterField(
            model_name="posta",
            name="prijemce",
            field=models.CharField(db_column="prijemce", max_length=25),
        ),
        migrations.AlterField(
            model_name="posta",
            name="viditelnost",
            field=models.CharField(db_column="viditelnost", max_length=1),
        ),
        migrations.RenameModel(
            old_name="Posta",
            new_name="Letters",
        ),
    ]
