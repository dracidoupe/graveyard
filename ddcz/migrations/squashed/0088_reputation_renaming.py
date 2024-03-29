# Generated by Django 2.0.13 on 2021-06-13 19:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0087_reputation_init"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reputationadditional",
            name="duvod_udeleni",
            field=models.CharField(db_column="duvod_udeleni", max_length=200),
        ),
        migrations.AlterField(
            model_name="reputationadditional",
            name="hodnota",
            field=models.IntegerField(db_column="hodnota"),
        ),
        migrations.AlterField(
            model_name="reputationadditional",
            name="prijal_nick",
            field=models.CharField(db_column="prijal_nick", max_length=25),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="akce",
            field=models.CharField(db_column="akce", max_length=3),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="dal",
            field=models.CharField(db_column="dal", max_length=30),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="id_zaznamu",
            field=models.AutoField(
                db_column="id_zaznamu", primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="id_prispevku",
            field=models.PositiveIntegerField(
                blank=True, db_column="id_prispevku", null=True
            ),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="prijal",
            field=models.CharField(db_column="prijal", max_length=30),
        ),
        migrations.AlterField(
            model_name="reputationlog",
            name="v_diskusi",
            field=models.CharField(
                blank=True, db_column="v_diskuzi", max_length=1, null=True
            ),
        ),
        migrations.RenameField(
            model_name="reputationadditional",
            old_name="hodnota",
            new_name="amount",
        ),
        migrations.RenameField(
            model_name="reputationadditional",
            old_name="prijal_nick",
            new_name="donee",
        ),
        migrations.RenameField(
            model_name="reputationadditional",
            old_name="duvod_udeleni",
            new_name="reason",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="akce",
            new_name="action",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="v_diskusi",
            new_name="discussion",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="prijal",
            new_name="donee",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="dal",
            new_name="donor",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="id_zaznamu",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="reputationlog",
            old_name="id_prispevku",
            new_name="post",
        ),
    ]
