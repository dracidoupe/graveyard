# Generated by Django 2.0.13 on 2021-06-28 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ddcz", "0092_notice_board"),
    ]
    # If created from scratch, Django wrongly infers the existence
    # of `id` column that is not in the original database and creates it
    # This is a problem when it then tries to migrate the primary key
    # as below and tries to drop the existing primary key
    # This is not needed in production since no primary key is present there
    if not settings.DATABASE_IS_SEEDED:
        operations = [
            migrations.RemoveField(
                model_name="taverntablenoticeboard",
                name="id",
            ),
        ]
    else:
        operations = []
    operations.append(
        migrations.AlterField(
            model_name="taverntablenoticeboard",
            name="tavern_table",
            field=models.OneToOneField(
                db_column="id_stolu",
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="ddcz.TavernTable",
            ),
        ),
    )
