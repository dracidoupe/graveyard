# Generated by Django 2.0.13 on 2021-04-16 16:45

from django.db import migrations


def fill_mentat_ids(apps, schema_editor):
    MentatNewbie = apps.get_model("ddcz", "MentatNewbie")
    i = 1
    for relation in MentatNewbie.objects.all():
        # can't do instance.save since that would check for integrity of PK
        MentatNewbie.objects.filter(
            mentat_id=relation.mentat_id, newbie_id=relation.newbie_id
        ).update(django_id=i)
        i += 1


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0063_mentatnewbie_django_id"),
    ]

    operations = [
        migrations.RunPython(fill_mentat_ids),
    ]
