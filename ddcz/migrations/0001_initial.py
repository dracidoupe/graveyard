import ddcz.models.magic

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AktivniUzivatele",
            fields=[
                (
                    "relid",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                ("id_uzivatele", models.IntegerField()),
                ("lastused", models.PositiveIntegerField()),
                ("agend", models.CharField(max_length=100)),
                ("ip", models.CharField(db_column="IP", max_length=15)),
                ("nck", models.CharField(max_length=50)),
                ("timelimit", models.IntegerField()),
                (
                    "relid_cookie",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
            ],
            options={
                "db_table": "aktivni_uzivatele",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Alchpredmety",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.CharField(max_length=30)),
                ("mag", models.IntegerField(blank=True, null=True)),
                ("suroviny", models.SmallIntegerField(blank=True, null=True)),
                ("zaklad", models.CharField(blank=True, max_length=150, null=True)),
                ("nalezeni", models.CharField(blank=True, max_length=150, null=True)),
                ("trvani", models.CharField(blank=True, max_length=30, null=True)),
                ("vyroba", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "nebezpecnost",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("sila", models.CharField(blank=True, max_length=30, null=True)),
                ("bcz", models.CharField(blank=True, max_length=30, null=True)),
                ("denmag", models.IntegerField(blank=True, null=True)),
                (
                    "dosah_ucinku",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("uroven_vyrobce", models.CharField(max_length=10)),
                ("sfera", models.CharField(max_length=20)),
                ("popis", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("autor", models.CharField(blank=True, max_length=25, null=True)),
                ("autmail", models.CharField(blank=True, max_length=30, null=True)),
                ("zdroj", models.CharField(blank=True, max_length=100, null=True)),
                ("zdrojmail", models.CharField(blank=True, max_length=40, null=True)),
                ("datum", models.DateTimeField()),
                ("schvaleno", models.CharField(max_length=1)),
                ("skupina", models.CharField(max_length=30)),
                ("tisknuto", models.SmallIntegerField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "alchpredmety",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Ankety",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("otazka", models.TextField(blank=True, null=True)),
                ("odp1", models.CharField(max_length=250)),
                ("p1", models.IntegerField()),
                ("odp2", models.CharField(max_length=250)),
                ("p2", models.IntegerField()),
                ("odp3", models.CharField(max_length=250)),
                ("p3", models.IntegerField()),
                ("odp4", models.CharField(max_length=250)),
                ("p4", models.IntegerField()),
                ("odp5", models.CharField(max_length=250)),
                ("p5", models.IntegerField()),
                ("odp6", models.CharField(max_length=250)),
                ("p6", models.IntegerField()),
                ("odp7", models.CharField(max_length=250)),
                ("p7", models.IntegerField()),
                ("odp8", models.CharField(max_length=250)),
                ("p8", models.IntegerField()),
                ("odp9", models.CharField(max_length=250)),
                ("p9", models.IntegerField()),
                ("odp10", models.CharField(max_length=250)),
                ("p10", models.IntegerField()),
                ("spusteno", models.IntegerField()),
                ("konec", models.IntegerField()),
                ("id_stolu", models.IntegerField()),
                ("jmenovite", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "ankety",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AnketyHlasy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("anketa_id", models.IntegerField()),
                ("user_id", models.IntegerField()),
                ("answer_id", models.IntegerField()),
                ("user_comment", models.CharField(max_length=1023)),
            ],
            options={
                "db_table": "ankety_hlasy",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="BannedIp",
            fields=[
                (
                    "ip",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("popis", models.CharField(max_length=64)),
            ],
            options={
                "db_table": "banned_ip",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Bestiar",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("zvt", models.TextField()),
                ("uc", models.TextField()),
                ("oc", models.TextField()),
                ("odl", models.CharField(max_length=3)),
                ("inteligence", models.CharField(blank=True, max_length=50, null=True)),
                ("vel", models.CharField(max_length=20)),
                ("zran", models.TextField(blank=True, null=True)),
                ("poh", models.TextField(blank=True, null=True)),
                ("pres", models.TextField(blank=True, null=True)),
                ("pokl", models.TextField(blank=True, null=True)),
                ("zkus", models.CharField(max_length=50)),
                ("popis", models.TextField()),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("pochvez", models.CharField(blank=True, max_length=1, null=True)),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("skupina", models.TextField()),
                ("bojovnost", models.CharField(blank=True, max_length=50, null=True)),
                ("sm", models.CharField(db_column="SM", max_length=50)),
                ("tisknuto", models.PositiveIntegerField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "bestiar",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Chat1",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chat1Zaloha",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat1_zaloha",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chat1Zaloha2",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat1_zaloha2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chat2",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chat3",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat_3",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Chat4",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pro", models.IntegerField()),
                ("od", models.IntegerField()),
                ("cas", models.IntegerField()),
                ("zprava", models.TextField()),
                ("nick", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "chat_4",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ChatAktivni",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nick", models.TextField(blank=True, null=True)),
                ("cas", models.IntegerField(blank=True, null=True)),
                ("mistnost", models.IntegerField()),
            ],
            options={
                "db_table": "chat_aktivni",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ChatMistnosti",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazev", models.CharField(max_length=40)),
                ("popis", models.CharField(max_length=255)),
                ("stala", models.IntegerField()),
                ("spravce", models.IntegerField()),
                ("septani", models.IntegerField()),
                ("zamknuto", models.IntegerField()),
                ("sprava", models.IntegerField()),
                ("bez_hostu", models.IntegerField()),
                ("duch", models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "chat_mistnosti",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ChatPristupy",
            fields=[
                (
                    "mistnost_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("nick", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "chat_pristupy",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ChatProperties",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_uz", models.PositiveIntegerField()),
                ("param", models.CharField(max_length=25)),
                ("value", models.CharField(max_length=25)),
            ],
            options={
                "db_table": "chat_properties",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="CommonArticles",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", ddcz.models.magic.MisencodedTextField()),
                ("text", ddcz.models.magic.MisencodedTextField()),
                (
                    "autor",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=25, null=True
                    ),
                ),
                (
                    "autmail",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=30, null=True
                    ),
                ),
                ("datum", models.DateTimeField()),
                (
                    "schvaleno",
                    ddcz.models.magic.MisencodedCharField(
                        choices=[("a", "Schváleno"), ("n", "Neschváleno")], max_length=1
                    ),
                ),
                ("zdroj", ddcz.models.magic.MisencodedTextField(blank=True, null=True)),
                (
                    "zdrojmail",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=30, null=True
                    ),
                ),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
                ("pochvez", ddcz.models.magic.MisencodedCharField(max_length=5)),
                ("precteno", models.IntegerField()),
                ("tisknuto", models.IntegerField()),
                (
                    "skupina",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=30, null=True
                    ),
                ),
                (
                    "anotace",
                    ddcz.models.magic.MisencodedTextField(blank=True, null=True),
                ),
                ("rubrika", ddcz.models.magic.MisencodedCharField(max_length=30)),
            ],
            options={
                "verbose_name": "Běžné příspěvky",
                "verbose_name_plural": "Běžné příspěvky",
                "db_table": "prispevky_dlouhe",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Diskuze",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_cizi", models.IntegerField()),
                ("nickname", models.CharField(max_length=25)),
                ("email", models.CharField(max_length=40)),
                ("text", models.TextField()),
                ("datum", models.DateTimeField()),
                ("cizi_tbl", models.CharField(max_length=20)),
                ("reputace", models.IntegerField()),
            ],
            options={
                "db_table": "diskuze",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="DiskuzeMaillist",
            fields=[
                ("id_uz", models.IntegerField(primary_key=True, serialize=False)),
                ("id_cizi", models.IntegerField()),
                ("email", models.CharField(max_length=40)),
                ("cizi_tbl", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "diskuze_maillist",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Dobrodruzstvi",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("anotace", models.TextField()),
                ("cesta", models.TextField(blank=True, null=True)),
                ("klicsl", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("pocet_hlasujicich", models.IntegerField()),
                ("hodnota_hlasovani", models.IntegerField()),
                ("precteno", models.IntegerField()),
            ],
            options={
                "db_table": "dobrodruzstvi",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Dovednosti",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("vlastnost", models.TextField()),
                ("obtiznost", models.TextField()),
                ("overovani", models.TextField()),
                ("totuspech", models.TextField()),
                ("uspech", models.TextField()),
                ("neuspech", models.TextField()),
                ("fatneuspech", models.TextField()),
                ("popis", models.TextField()),
                ("autor", models.TextField()),
                ("autmail", models.TextField()),
                ("zdroj", models.TextField()),
                ("zdrojmail", models.TextField()),
                ("schvaleno", models.CharField(max_length=1)),
                ("datum", models.DateTimeField()),
                ("tisknuto", models.PositiveIntegerField()),
                ("pochvez", models.CharField(max_length=1)),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
                ("hlasoval", models.TextField(blank=True, null=True)),
                ("precteno", models.IntegerField()),
                ("skupina", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "dovednosti",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Downloady",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("cesta", models.TextField(blank=True, null=True)),
                ("pochvez", models.CharField(max_length=1)),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("format", models.TextField()),
                ("popis", models.TextField()),
                ("velikost", models.IntegerField()),
                ("skupina", models.TextField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "downloady",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Duchovo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datum", models.IntegerField()),
                ("param", models.CharField(max_length=15)),
                ("value", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "duchovo",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Duchovo1",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datum", models.IntegerField()),
                ("param", models.CharField(max_length=15)),
                ("value", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "duchovo1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Forum",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nickname", models.CharField(max_length=64)),
                ("email", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("text", models.TextField()),
                ("reg", models.CharField(max_length=50)),
                ("reputace", models.IntegerField()),
            ],
            options={
                "db_table": "forum",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Forums",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("active", models.SmallIntegerField()),
                ("description", models.CharField(max_length=255)),
                ("config_suffix", models.CharField(max_length=50)),
                ("folder", models.CharField(max_length=1)),
                ("parent", models.IntegerField()),
                ("display", models.PositiveIntegerField()),
                ("table_name", models.CharField(max_length=50)),
                ("moderation", models.CharField(max_length=1)),
                ("email_list", models.CharField(max_length=50)),
                ("email_return", models.CharField(max_length=50)),
                ("email_tag", models.CharField(max_length=50)),
                ("check_dup", models.PositiveSmallIntegerField()),
                ("multi_level", models.PositiveSmallIntegerField()),
                ("collapse", models.PositiveSmallIntegerField()),
                ("flat", models.PositiveSmallIntegerField()),
                ("lang", models.CharField(max_length=50)),
                ("html", models.CharField(max_length=40)),
                ("table_width", models.CharField(max_length=4)),
                ("table_header_color", models.CharField(max_length=7)),
                ("table_header_font_color", models.CharField(max_length=7)),
                ("table_body_color_1", models.CharField(max_length=7)),
                ("table_body_color_2", models.CharField(max_length=7)),
                ("table_body_font_color_1", models.CharField(max_length=7)),
                ("table_body_font_color_2", models.CharField(max_length=7)),
                ("nav_color", models.CharField(max_length=7)),
                ("nav_font_color", models.CharField(max_length=7)),
                ("allow_uploads", models.CharField(max_length=1)),
                ("upload_types", models.CharField(max_length=100)),
                ("upload_size", models.PositiveIntegerField()),
                ("max_uploads", models.PositiveIntegerField()),
                ("security", models.PositiveIntegerField()),
                ("showip", models.PositiveSmallIntegerField()),
                ("emailnotification", models.PositiveSmallIntegerField()),
                ("body_color", models.CharField(max_length=7)),
                ("body_link_color", models.CharField(max_length=7)),
                ("body_alink_color", models.CharField(max_length=7)),
                ("body_vlink_color", models.CharField(max_length=7)),
                ("required_level", models.SmallIntegerField()),
                ("permissions", models.SmallIntegerField()),
                ("allow_edit", models.SmallIntegerField()),
                ("allow_langsel", models.SmallIntegerField()),
                ("displayflag", models.SmallIntegerField()),
            ],
            options={
                "db_table": "forums",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ForumsAuth",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=200)),
                ("webpage", models.CharField(max_length=200)),
                ("image", models.CharField(max_length=200)),
                ("icq", models.CharField(max_length=50)),
                ("aol", models.CharField(max_length=50)),
                ("yahoo", models.CharField(max_length=50)),
                ("msn", models.CharField(max_length=50)),
                ("jabber", models.CharField(max_length=50)),
                ("signature", models.CharField(max_length=255)),
                ("max_group_permission_level", models.PositiveIntegerField()),
                ("permission_level", models.PositiveIntegerField()),
                ("hide_email", models.PositiveIntegerField()),
                ("lang", models.CharField(max_length=50)),
                ("password_tmp", models.CharField(max_length=50)),
                ("combined_token", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "forums_auth",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ForumsForum2Group",
            fields=[
                ("forum_id", models.PositiveIntegerField()),
                (
                    "group_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "forums_forum2group",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ForumsGroups",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("permission_level", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "forums_groups",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ForumsModerators",
            fields=[
                (
                    "user_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("forum_id", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "forums_moderators",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Fotogalerie",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.TextField()),
                ("cesta", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("cestathumb", models.TextField()),
            ],
            options={
                "db_table": "fotogalerie",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Galerie",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.TextField()),
                ("cesta", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("cestathumb", models.TextField()),
            ],
            options={
                "db_table": "galerie",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Grouplimits",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_uz", models.IntegerField()),
                ("max_soukr", models.SmallIntegerField(blank=True, null=True)),
                ("max_verej", models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "grouplimits",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Groupmembers",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_skupiny", models.IntegerField()),
                ("id_uz", models.IntegerField()),
                ("clenstvi", models.IntegerField(blank=True, null=True)),
                ("caszmeny", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "groupmembers",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="HlasovaniPrispevky",
            fields=[
                ("id_uz", models.IntegerField(primary_key=True, serialize=False)),
                ("id_cizi", models.IntegerField()),
                ("rubrika", models.CharField(max_length=20)),
                ("pochvez", models.IntegerField()),
                ("time", models.IntegerField()),
                ("opraveno", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "hlasovani_prispevky",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Hranicarkouzla",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("mag", models.SmallIntegerField()),
                ("magpop", models.TextField()),
                ("dosah", models.SmallIntegerField(blank=True, null=True)),
                ("dosahpop", models.TextField(blank=True, null=True)),
                ("rozsah", models.SmallIntegerField(blank=True, null=True)),
                ("rozsahpop", models.TextField(blank=True, null=True)),
                ("vyvolani", models.SmallIntegerField(blank=True, null=True)),
                ("vyvolanipop", models.TextField(blank=True, null=True)),
                ("druh", models.TextField(blank=True, null=True)),
                ("skupina", models.TextField()),
                ("cetnost", models.TextField(blank=True, null=True)),
                ("pomucky", models.TextField(blank=True, null=True)),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("datum", models.DateTimeField()),
                ("pochvez", models.CharField(max_length=1)),
                ("popis", models.TextField()),
                ("tisknuto", models.IntegerField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "hranicarkouzla",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Inzerce",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sekce", models.CharField(max_length=20)),
                ("jmeno", models.CharField(blank=True, max_length=30, null=True)),
                ("mail", models.CharField(blank=True, max_length=30, null=True)),
                ("telefon", models.CharField(blank=True, max_length=15, null=True)),
                ("mobil", models.CharField(blank=True, max_length=15, null=True)),
                ("okres", models.CharField(blank=True, max_length=20, null=True)),
                ("text", models.TextField()),
                ("datum", models.CharField(max_length=12)),
            ],
            options={
                "db_table": "inzerce",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Kouzla",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("kouzsl", models.TextField()),
                ("mag", models.SmallIntegerField()),
                ("magpop", models.TextField()),
                ("past", models.TextField(blank=True, null=True)),
                ("dosah", models.IntegerField(blank=True, null=True)),
                ("dosahpop", models.TextField(blank=True, null=True)),
                ("rozsah", models.IntegerField()),
                ("rozsahpop", models.TextField(blank=True, null=True)),
                ("vyvolani", models.IntegerField()),
                ("vyvolanipop", models.TextField()),
                ("trvani", models.IntegerField()),
                ("trvanipop", models.TextField(blank=True, null=True)),
                ("popis", models.TextField()),
                ("skupina", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("datum", models.DateTimeField()),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("tisknuto", models.PositiveIntegerField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "kouzla",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="LevelParametry2",
            fields=[
                (
                    "parametr",
                    ddcz.models.magic.MisencodedCharField(
                        max_length=40, primary_key=True, serialize=False
                    ),
                ),
                ("hodnota", ddcz.models.magic.MisencodedCharField(max_length=30)),
            ],
            options={
                "db_table": "level_parametry_2",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Limity",
            fields=[
                (
                    "oprava_hlasovani_po",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("platnost", models.CharField(max_length=1)),
                ("oprava_hlasovani_pred", models.IntegerField()),
                ("platnost_limitu_pred", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "limity",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Linky",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazev", models.TextField()),
                ("adresa", models.TextField()),
                ("popis", models.TextField()),
                ("pochvez", models.CharField(max_length=1)),
                ("schvaleno", models.CharField(max_length=1)),
                ("datum", models.DateTimeField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "linky",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Mailgroups",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("verejna", models.CharField(max_length=3)),
                ("nazev_skupiny", models.CharField(max_length=30, unique=True)),
            ],
            options={
                "db_table": "mailgroups",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MaillistCeka",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rubrika", models.CharField(max_length=30)),
                ("data", models.TextField()),
                ("dataplain", models.TextField()),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "maillist_ceka",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MentatNewbie",
            fields=[
                ("newbie_id", models.IntegerField(primary_key=True, serialize=False)),
                ("mentat_id", models.IntegerField()),
                ("newbie_rate", models.IntegerField()),
                ("mentat_rate", models.IntegerField()),
                ("locked", models.CharField(max_length=2)),
                ("penalty", models.IntegerField()),
            ],
            options={
                "db_table": "mentat_newbie",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="MentatsAvail",
            fields=[
                ("user_id", models.IntegerField(primary_key=True, serialize=False)),
                ("intro_m", models.TextField()),
                ("intro_z", models.TextField()),
            ],
            options={
                "db_table": "mentats_avail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsDilna",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_dilna",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsDilnaAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_dilna_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsDilnaBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_dilna_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsDracidoupecz",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_dracidoupecz",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsDracidoupeczBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_dracidoupecz_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsGalerieDilna",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_galerie_dilna",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsGalerieDilnaAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_galerie_dilna_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsGalerieDilnaBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_galerie_dilna_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsHtmldilna",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_htmldilna",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsHtmldilnaAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_htmldilna_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsHtmldilnaBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_htmldilna_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsOstatni",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_ostatni",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsOstatniAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_ostatni_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsOstatniBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_ostatni_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPj",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_pj",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPjAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_pj_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPjBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_pj_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPravidla",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_pravidla",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPravidlaAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_pravidla_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsPravidlaBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_pravidla_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRing",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_ring",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRingAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_ring_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRingBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_ring_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRoleplaying",
            fields=[
                ("id", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("datestamp", models.DateTimeField()),
                ("thread", models.PositiveIntegerField()),
                ("parent", models.PositiveIntegerField()),
                ("author", models.CharField(max_length=37)),
                ("subject", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=200)),
                ("host", models.CharField(max_length=255)),
                ("email_reply", models.CharField(max_length=1)),
                ("approved", models.CharField(max_length=1)),
                ("msgid", models.CharField(max_length=100)),
                ("modifystamp", models.PositiveIntegerField()),
                ("userid", models.PositiveIntegerField()),
                ("closed", models.IntegerField()),
            ],
            options={
                "db_table": "ms_roleplaying",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRoleplayingAttachments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_id", models.PositiveIntegerField()),
                ("filename", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "ms_roleplaying_attachments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="MsRoleplayingBodies",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("thread", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "ms_roleplaying_bodies",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Navstevnost",
            fields=[
                (
                    "ip",
                    models.CharField(max_length=16, primary_key=True, serialize=False),
                ),
                ("naposled", models.DateTimeField()),
            ],
            options={
                "db_table": "navstevnost",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datum", models.DateTimeField()),
                ("autor", ddcz.models.magic.MisencodedTextField()),
                ("autmail", ddcz.models.magic.MisencodedTextField()),
                ("text", ddcz.models.magic.MisencodedTextField()),
            ],
            options={
                "verbose_name": "Aktuality",
                "verbose_name_plural": "Aktuality",
                "db_table": "aktuality",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Posta",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("odesilatel", models.CharField(max_length=25)),
                ("prijemce", models.CharField(max_length=25)),
                ("viditelnost", models.CharField(max_length=1)),
                ("text", models.TextField()),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "posta",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Pravomoci",
            fields=[
                ("id_user", models.IntegerField(primary_key=True, serialize=False)),
                ("funkce", models.CharField(max_length=20)),
                ("stupen", models.IntegerField()),
            ],
            options={
                "db_table": "pravomoci",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Predmety",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.TextField()),
                ("uc", models.TextField(blank=True, db_column="UC", null=True)),
                (
                    "kz",
                    models.CharField(
                        blank=True, db_column="KZ", max_length=3, null=True
                    ),
                ),
                ("delka", models.CharField(blank=True, max_length=3, null=True)),
                ("cena", models.IntegerField()),
                ("popis", models.TextField()),
                ("autor", models.TextField(blank=True, null=True)),
                ("autmail", models.TextField(blank=True, null=True)),
                ("datum", models.DateTimeField()),
                ("pochvez", models.CharField(max_length=1)),
                ("malydostrel", models.IntegerField(blank=True, null=True)),
                ("strednidostrel", models.IntegerField(blank=True, null=True)),
                ("velkydostrel", models.IntegerField(blank=True, null=True)),
                ("sfera", models.IntegerField(blank=True, null=True)),
                ("vaha", models.IntegerField()),
                ("zdroj", models.TextField(blank=True, null=True)),
                ("zdrojmail", models.TextField(blank=True, null=True)),
                ("schvaleno", models.CharField(max_length=1)),
                ("skupina", models.TextField()),
                ("tisknuto", models.SmallIntegerField()),
                ("pocet_hlasujicich", models.IntegerField(blank=True, null=True)),
                ("hodnota_hlasovani", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "predmety",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="PsiSmecka",
            fields=[
                ("id_uz", models.IntegerField(primary_key=True, serialize=False)),
                ("cizi_tbl", models.CharField(max_length=20)),
                ("id_dilo", models.IntegerField()),
                ("navstiveno", models.IntegerField()),
                ("neprectenych", models.IntegerField()),
            ],
            options={
                "db_table": "psi_smecka",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaBook",
            fields=[
                ("id_stolu", models.IntegerField(primary_key=True, serialize=False)),
                ("id_uz", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_book",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaLinky",
            fields=[
                ("id_stolu", models.IntegerField(primary_key=True, serialize=False)),
                ("id_linku", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_linky",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaNastenky",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_stolu", models.IntegerField(unique=True)),
                ("nazev_stolu", models.CharField(max_length=128)),
                ("text_nastenky", models.TextField()),
                ("posledni_zmena", models.DateTimeField(blank=True, null=True)),
                ("zmenil", models.CharField(max_length=25)),
            ],
            options={
                "db_table": "putyka_nastenky",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaNavstevnost",
            fields=[
                ("cas", models.DateTimeField(primary_key=True, serialize=False)),
                ("misto", models.CharField(max_length=31)),
                ("pocet", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_navstevnost",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaNeoblibene",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_uz", models.IntegerField()),
                ("id_stolu", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_neoblibene",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaPrispevky",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_stolu", models.IntegerField()),
                ("text", models.TextField()),
                ("autor", models.CharField(max_length=30)),
                ("reputace", models.IntegerField()),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "putyka_prispevky",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaPristup",
            fields=[
                ("id_stolu", models.IntegerField(primary_key=True, serialize=False)),
                ("typ_pristupu", models.CharField(max_length=5)),
                ("nick_usera", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "putyka_pristup",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaSekce",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("kod", models.IntegerField()),
                ("poradi", models.IntegerField()),
                ("nazev", models.CharField(max_length=50)),
                ("popis", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "putyka_sekce",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaSlucovani",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_ja", models.IntegerField()),
                ("id_on", models.IntegerField()),
                ("zustavam", models.SmallIntegerField()),
                ("oznaceni", models.CharField(max_length=60)),
            ],
            options={
                "db_table": "putyka_slucovani",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaStoly",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.CharField(max_length=255, unique=True)),
                ("popis", models.CharField(max_length=255)),
                ("vlastnik", models.CharField(max_length=30)),
                ("povol_hodnoceni", models.CharField(max_length=1)),
                ("min_level", models.CharField(max_length=1)),
                ("zalozen", models.DateTimeField()),
                ("verejny", models.CharField(max_length=1)),
                ("celkem", models.IntegerField(blank=True, null=True)),
                ("sekce", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_stoly",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PutykaUzivatele",
            fields=[
                ("id_stolu", models.IntegerField(primary_key=True, serialize=False)),
                ("id_uzivatele", models.IntegerField()),
                ("oblibenost", models.IntegerField()),
                ("navstiveno", models.DateTimeField(blank=True, null=True)),
                ("neprectenych", models.IntegerField(blank=True, null=True)),
                ("sprava", models.IntegerField()),
                ("pristup", models.IntegerField()),
            ],
            options={
                "db_table": "putyka_uzivatele",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaBanneryZasobnik",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vlastnik", models.IntegerField()),
                ("cesta", models.CharField(blank=True, max_length=60, null=True)),
                ("cislo", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "reklama_bannery_zasobnik",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaKampaneBannery",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vlastnik", models.IntegerField()),
                ("cesta", models.CharField(max_length=60)),
                ("odkaz", models.CharField(max_length=60)),
                ("imp_zadane", models.IntegerField()),
                ("imp_zobrazene", models.IntegerField()),
                ("poc_kliku", models.IntegerField()),
                ("zacatek", models.DateTimeField()),
            ],
            options={
                "db_table": "reklama_kampane_bannery",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaKampaneText",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vlastnik", models.IntegerField()),
                ("text", models.CharField(max_length=255)),
                ("odkaz", models.CharField(max_length=60)),
                ("bezici", models.CharField(max_length=1)),
                ("imp_zadane", models.IntegerField()),
                ("imp_zobrazene", models.IntegerField()),
                ("poc_kliku", models.IntegerField()),
                ("zacatek", models.DateTimeField()),
            ],
            options={
                "db_table": "reklama_kampane_text",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaMail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("k_roz", models.PositiveIntegerField()),
                ("rozeslano", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "reklama_mail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaUkoncene",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vlastnik", models.IntegerField()),
                ("imp_zobrazene", models.IntegerField()),
                ("poc_kliku", models.IntegerField()),
                ("zacatek", models.DateTimeField()),
                ("konec", models.DateTimeField()),
                ("typ", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "reklama_ukoncene",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReklamaUsers",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("loginname", models.CharField(max_length=30)),
                ("heslo", models.CharField(max_length=35)),
                ("email", models.CharField(max_length=30)),
                ("imprese_ban", models.IntegerField()),
                ("imprese_txt", models.IntegerField()),
                ("info", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "reklama_users",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReputaceLog",
            fields=[
                ("id_zaznamu", models.AutoField(primary_key=True, serialize=False)),
                ("dal", models.CharField(max_length=30)),
                ("prijal", models.CharField(max_length=30)),
                ("akce", models.CharField(max_length=3)),
                ("v_diskusi", models.CharField(blank=True, max_length=1, null=True)),
                ("id_prispevku", models.PositiveIntegerField(blank=True, null=True)),
                ("date", models.IntegerField()),
            ],
            options={
                "db_table": "reputace_log",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReputaceSpecial",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prijal_nick", models.CharField(max_length=25)),
                ("duvod_udeleni", models.CharField(max_length=200)),
                ("hodnota", models.IntegerField()),
            ],
            options={
                "db_table": "reputace_special",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="RubrikyPristup",
            fields=[
                (
                    "id_usr",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                ("id_cizi", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "rubriky_pristup",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Runy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_darce", models.IntegerField()),
                ("nick_darce", models.CharField(max_length=30)),
                ("id_prijemce", models.IntegerField(blank=True, null=True)),
                ("nick_prijemce", models.CharField(max_length=30)),
                ("typ", models.CharField(max_length=15)),
                ("grafika", models.SmallIntegerField()),
                ("venovani", models.TextField()),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "runy",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Seznamka",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jmeno", models.CharField(blank=True, max_length=40, null=True)),
                ("email", models.CharField(blank=True, max_length=40, null=True)),
                ("telefon", models.CharField(blank=True, max_length=20, null=True)),
                ("mobil", models.CharField(blank=True, max_length=20, null=True)),
                ("vek", models.IntegerField(blank=True, null=True)),
                ("okres", models.CharField(blank=True, max_length=40, null=True)),
                ("doba", models.CharField(blank=True, max_length=20, null=True)),
                ("datum", models.DateTimeField(blank=True, null=True)),
                ("text", models.TextField(blank=True, null=True)),
                ("sekce", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                "db_table": "seznamka",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="Skiny",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nazev", models.CharField(max_length=10)),
                ("jmeno", models.CharField(max_length=50)),
                ("autor", models.CharField(max_length=20)),
                ("autmail", models.CharField(max_length=40)),
                ("popis", models.TextField()),
            ],
            options={
                "db_table": "skiny",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Slovnicek",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jazyk", models.IntegerField()),
                ("kat", models.CharField(max_length=33)),
                ("cis", models.CharField(max_length=7)),
                ("rod", models.CharField(max_length=9)),
                ("spc1", models.SmallIntegerField()),
                ("spc2", models.SmallIntegerField()),
                ("text", models.CharField(max_length=40)),
            ],
            options={
                "db_table": "slovnicek",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="SortPrim",
            fields=[
                (
                    "autor",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                ("prumer", models.CharField(max_length=3)),
                ("pocet_prispevku", models.IntegerField()),
                ("pocet_v_diskuzi", models.IntegerField()),
                ("reputace", models.IntegerField()),
                ("level", models.CharField(max_length=1)),
                ("level_new", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "sort_prim",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Spravci",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("loginname", models.CharField(max_length=200)),
                ("pass_field", models.CharField(db_column="pass", max_length=32)),
                ("rubaktuality", models.CharField(max_length=1)),
                ("hrbitov", models.CharField(max_length=1)),
                ("rubdobrodruzstvi", models.CharField(max_length=1)),
                ("rubclanky", models.CharField(max_length=1)),
                ("rublinky", models.CharField(max_length=1)),
                ("rubbestiar", models.CharField(max_length=1)),
                ("rubvalecnik", models.CharField(max_length=1)),
                ("rubhranicar", models.CharField(max_length=1)),
                ("rubalchymista", models.CharField(max_length=1)),
                ("rubkouzelnik", models.CharField(max_length=1)),
                ("rubzlodej", models.CharField(max_length=1)),
                ("rubnovapovolani", models.CharField(max_length=1)),
                ("mail", models.CharField(max_length=255)),
                ("rubpredmety", models.CharField(max_length=1)),
                ("rubdownloady", models.CharField(max_length=1)),
                ("rubgalerie", models.CharField(max_length=1)),
                ("rubdovednosti", models.CharField(max_length=1)),
                ("rubnoverasy", models.CharField(max_length=1)),
                ("uzivatele", models.CharField(max_length=1)),
                ("rubexpanze", models.CharField(max_length=1)),
                ("alchpred", models.CharField(max_length=1)),
                ("hrankouzla", models.CharField(max_length=1)),
                ("kkouzla", models.CharField(max_length=1)),
                ("rubputyka", models.CharField(max_length=1)),
                ("rubprogram", models.CharField(max_length=1)),
                ("rubms", models.CharField(db_column="rubMS", max_length=1)),
                ("rubfotogalerie", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "spravci",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="StatistikyAutori",
            fields=[
                (
                    "autor",
                    models.CharField(max_length=25, primary_key=True, serialize=False),
                ),
                ("rubrika", models.CharField(max_length=25)),
                ("pocet", models.IntegerField()),
            ],
            options={
                "db_table": "statistiky_autori",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="StatistikyDila",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("autor", models.CharField(max_length=32)),
                ("rubrika", models.CharField(max_length=32)),
                ("skupina", models.CharField(max_length=32)),
                ("hodnoceni", models.FloatField()),
                ("datum", models.DateTimeField()),
            ],
            options={
                "db_table": "statistiky_dila",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UserRatings",
            fields=[
                ("record_id", models.AutoField(primary_key=True, serialize=False)),
                ("rating_time", models.IntegerField()),
                ("byfk", models.IntegerField(db_column="byFK")),
                ("forfk", models.IntegerField(db_column="forFK")),
                ("visible", models.SmallIntegerField()),
                ("rating_text", models.TextField()),
            ],
            options={
                "db_table": "user_ratings",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UserStats",
            fields=[
                ("user_id", models.IntegerField(primary_key=True, serialize=False)),
                ("loghistory", models.CharField(max_length=200)),
            ],
            options={
                "db_table": "user_stats",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Uzivatele",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "jmeno_uzivatele",
                    ddcz.models.magic.MisencodedCharField(max_length=20),
                ),
                (
                    "nick_uzivatele",
                    ddcz.models.magic.MisencodedCharField(max_length=25, unique=True),
                ),
                (
                    "prijmeni_uzivatele",
                    ddcz.models.magic.MisencodedCharField(max_length=20),
                ),
                ("psw_uzivatele", ddcz.models.magic.MisencodedCharField(max_length=40)),
                (
                    "email_uzivatele",
                    ddcz.models.magic.MisencodedCharField(max_length=50),
                ),
                (
                    "pohlavi_uzivatele",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=4, null=True
                    ),
                ),
                ("vek_uzivatele", models.IntegerField()),
                (
                    "kraj_uzivatele",
                    ddcz.models.magic.MisencodedCharField(max_length=20),
                ),
                ("chat_barva", ddcz.models.magic.MisencodedCharField(max_length=6)),
                ("chat_pismo", models.IntegerField()),
                ("chat_reload", models.IntegerField()),
                ("chat_zprav", models.IntegerField()),
                (
                    "chat_filtr",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=255, null=True
                    ),
                ),
                ("chat_filtr_zobrazit", models.IntegerField()),
                ("pospristup", models.DateTimeField()),
                ("level", ddcz.models.magic.MisencodedCharField(max_length=1)),
                ("icq_uzivatele", models.IntegerField()),
                ("vypsat_udaje", ddcz.models.magic.MisencodedCharField(max_length=15)),
                (
                    "ikonka_uzivatele",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=25, null=True
                    ),
                ),
                (
                    "popis_uzivatele",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=255, null=True
                    ),
                ),
                ("nova_posta", models.IntegerField()),
                ("skin", ddcz.models.magic.MisencodedCharField(max_length=10)),
                ("reputace", models.IntegerField()),
                ("reputace_rozdel", models.PositiveIntegerField()),
                ("status", ddcz.models.magic.MisencodedCharField(max_length=1)),
                ("reg_schval_datum", models.DateTimeField(blank=True, null=True)),
                (
                    "indexhodnotitele",
                    models.DecimalField(decimal_places=2, max_digits=4),
                ),
                ("reload", ddcz.models.magic.MisencodedCharField(max_length=1)),
                ("max_level", models.IntegerField(blank=True, null=True)),
                (
                    "api_key",
                    ddcz.models.magic.MisencodedCharField(
                        blank=True, max_length=40, null=True, unique=True
                    ),
                ),
            ],
            options={
                "db_table": "uzivatele",
                "managed": not settings.DATABASE_IS_SEEDED,
            },
        ),
        migrations.CreateModel(
            name="UzivateleCekajici",
            fields=[
                ("id_zaznamu", models.AutoField(primary_key=True, serialize=False)),
                ("nick_uzivatele", models.CharField(max_length=30, unique=True)),
                ("email", models.CharField(max_length=40, unique=True)),
                ("jmeno", models.CharField(max_length=40)),
                ("prijmeni", models.CharField(max_length=40)),
                ("pohlavi", models.CharField(max_length=4)),
                ("datum", models.IntegerField()),
                ("patron", models.IntegerField()),
                ("primluvy", models.IntegerField()),
                ("osloveni", models.CharField(blank=True, max_length=50, null=True)),
                ("popis_text", models.TextField()),
            ],
            options={
                "db_table": "uzivatele_cekajici",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UzivateleFiltry",
            fields=[
                ("id_uz", models.IntegerField(primary_key=True, serialize=False)),
                ("rubrika", models.CharField(max_length=20)),
                ("filtr", models.CharField(max_length=15)),
                ("hodnota", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "uzivatele_filtry",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UzivateleMaillist",
            fields=[
                ("id_uz", models.IntegerField(primary_key=True, serialize=False)),
                ("rubrika", models.CharField(max_length=20)),
                ("email_uz", models.CharField(max_length=40)),
                ("mime", models.CharField(db_column="MIME", max_length=1)),
            ],
            options={
                "db_table": "uzivatele_maillist",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="UzivateleZamitnuti",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nick_uzivatele", models.CharField(max_length=30)),
                ("email", models.CharField(max_length=50)),
                ("jmeno", models.CharField(max_length=40)),
                ("prijmeni", models.CharField(max_length=40)),
                ("pohlavi", models.CharField(max_length=4)),
                ("datum", models.IntegerField()),
            ],
            options={
                "db_table": "uzivatele_zamitnuti",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldHlasovani",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
                ("rocnik", models.CharField(max_length=6)),
            ],
            options={
                "db_table": "zld_hlasovani",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldMain",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rocnik", models.CharField(max_length=6, unique=True)),
                ("status", models.CharField(max_length=1)),
            ],
            options={
                "db_table": "zld_main",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("rocnik", models.CharField(max_length=6)),
            ],
            options={
                "db_table": "zld_nominace",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20012",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2001_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20012Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2001_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20021",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2002_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20021Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2002_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20022",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2002_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20022Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2002_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20031",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2003_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20031Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2003_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20032",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2003_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20032Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2003_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20041",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2004_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20041Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2004_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20042",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2004_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20042Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2004_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20051",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2005_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20051Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2005_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20052",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2005_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20052Hlasoval",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_usr", models.IntegerField()),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2005_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20061",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2006_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20061Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2006_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20062",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2006_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20062Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2006_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20071",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2007_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20071Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2007_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20072",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2007_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20072Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2007_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20081",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2008_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20081Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2008_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20082",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2008_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20082Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2008_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20091",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2009_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20091Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2009_1_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20092",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cizi_id", models.IntegerField()),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_nominace_2009_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldNominace20092Hlasoval",
            fields=[
                ("id_usr", models.IntegerField(primary_key=True, serialize=False)),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.CharField(max_length=3)),
            ],
            options={
                "db_table": "zld_nominace_2009_2_hlasoval",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20012",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2001_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20021",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2002_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20022",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2002_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20031",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2003_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20032",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2003_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20041",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2004_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20042",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2004_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20051",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2005_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20052",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2005_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20061",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2006_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20062",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2006_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20071",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2007_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20072",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2007_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20081",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2008_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20082",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2008_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20091",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2009_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam20092",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2009_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam2010",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2010",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam2011",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2011",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam2012",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2012",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldPocitam2013",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_prispevku", models.IntegerField()),
                ("rubrika", models.CharField(max_length=30)),
                ("pocet_bodu", models.IntegerField()),
                ("misto1", models.IntegerField()),
                ("misto2", models.IntegerField()),
                ("misto3", models.IntegerField()),
                ("cernyd", models.IntegerField()),
            ],
            options={
                "db_table": "zld_pocitam_2013",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
                ("rocnik", models.CharField(max_length=6)),
            ],
            options={
                "db_table": "zld_vitezove",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20012",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2001_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20021",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2002_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20022",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2002_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20031",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2003_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20032",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2003_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20041",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2004_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20042",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2004_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20051",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2005_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20052",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2005_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20061",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2006_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20062",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2006_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20071",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2007_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20072",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2007_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20081",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2008_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20082",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2008_2",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20091",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2009_1",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ZldVitezove20092",
            fields=[
                ("cizi_id", models.IntegerField(primary_key=True, serialize=False)),
                ("jmeno", models.CharField(max_length=255)),
                ("rubrika", models.CharField(max_length=30)),
                ("autor", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "zld_vitezove_2009_2",
                "managed": False,
            },
        ),
    ]
