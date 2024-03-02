from django.db import migrations


def fill_relation_table_ids(apps, schema_editor):
    CreationVote = apps.get_model("ddcz", "CreationVote")
    i = 1

    for relation in CreationVote.objects.all():
        CreationVote.objects.filter(
            user_profile_id=relation.user_profile_id,
            creation_id=relation.creation_id,
            creative_page_slug=relation.creative_page_slug,
        ).update(django_id=i)
        i += 1


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0121_creationvote_django_id"),
    ]

    operations = [
        migrations.RunPython(fill_relation_table_ids),
    ]
