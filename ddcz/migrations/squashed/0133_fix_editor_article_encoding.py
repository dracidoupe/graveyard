# Generated by Django 2.0.13 on 2024-02-25 14:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ddcz", "0132_editor_article_20240225_1530"),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE ddcz_editorarticle CONVERT TO CHARACTER SET latin2 COLLATE latin2_czech_cs;"
        ),
        migrations.RunSQL(
            "ALTER TABLE ddcz_editorarticle MODIFY title VARCHAR(40) CHARACTER SET latin2 COLLATE latin2_czech_cs;"
        ),
        migrations.RunSQL(
            "ALTER TABLE ddcz_editorarticle MODIFY slug VARCHAR(40) CHARACTER SET latin2 COLLATE latin2_czech_cs;"
        ),
        migrations.RunSQL(
            "ALTER TABLE ddcz_editorarticle MODIFY text LONGTEXT CHARACTER SET latin2 COLLATE latin2_czech_cs;"
        ),
    ]
