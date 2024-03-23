from django.db import migrations

# When migrating from unmanaged to managed models,
# CreateModel must be explicitly used in order for table
# to be created in tests


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel("Uzivatele", "UserProfile"),
        migrations.RenameModel("Seznamka", "Dating"),
    ]
