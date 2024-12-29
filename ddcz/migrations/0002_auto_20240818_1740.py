# Generated by Django 3.1.14 on 2024-08-18 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0001_initial-post-switch-setup"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PutykaNeoblibene",
        ),
        migrations.AlterModelOptions(
            name="awaitingregistration",
            options={
                "verbose_name": "Uživatel ke schválení",
                "verbose_name_plural": "Uživatelé ke schválení",
            },
        ),
        migrations.AddField(
            model_name="awaitingregistration",
            name="age",
            field=models.IntegerField(db_column="vek", default=0),
            preserve_default=False,
        ),
    ]