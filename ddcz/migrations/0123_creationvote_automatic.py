from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0122_creationvote_datafill"),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE `hlasovani_prispevky` DROP PRIMARY KEY;"),
        migrations.RunSQL(
            "ALTER TABLE hlasovani_prispevky MODIFY django_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY;"
        ),
        migrations.RunSQL(
            """
                SET @m = (SELECT IFNULL(MAX(django_id) + 1, 1) FROM hlasovani_prispevky);
                SET @s = CONCAT('ALTER TABLE hlasovani_prispevky AUTO_INCREMENT=', @m);
                PREPARE stmt1 FROM @s;
                EXECUTE stmt1;
                DEALLOCATE PREPARE stmt1;
            """
        ),
    ]
