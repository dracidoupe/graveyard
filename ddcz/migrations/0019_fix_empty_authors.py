from django.db import migrations
from django.db.models import Q


def fix_empty_authors(apps, schema_editor):
    Author = apps.get_model("ddcz", "Author")
    # Fix authors with all identifying fields empty or null
    Author.objects.filter(
        Q(website="") | Q(website__isnull=True),
        Q(anonymous_user_nick="") | Q(anonymous_user_nick__isnull=True),
        Q(user_nick="") | Q(user_nick__isnull=True),
        user__isnull=True,
    ).update(website="Neznámý")


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0018_auto_20260321_0633"),
    ]

    operations = [
        migrations.RunPython(fix_empty_authors, reverse_code=migrations.RunPython.noop),
    ]
