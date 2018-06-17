# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class AktivniUzivatele(models.Model):
    relid = models.CharField(primary_key=True, max_length=32)
    id_uzivatele = models.IntegerField()
    lastused = models.PositiveIntegerField()
    agend = models.CharField(max_length=100)
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    nck = models.CharField(max_length=50)
    timelimit = models.IntegerField()
    relid_cookie = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aktivni_uzivatele'



class Alchpredmety(models.Model):
    jmeno = models.CharField(max_length=30)
    mag = models.IntegerField(blank=True, null=True)
    suroviny = models.SmallIntegerField(blank=True, null=True)
    zaklad = models.CharField(max_length=150, blank=True, null=True)
    nalezeni = models.CharField(max_length=150, blank=True, null=True)
    trvani = models.CharField(max_length=30, blank=True, null=True)
    vyroba = models.CharField(max_length=30, blank=True, null=True)
    nebezpecnost = models.CharField(max_length=30, blank=True, null=True)
    sila = models.CharField(max_length=30, blank=True, null=True)
    bcz = models.CharField(max_length=30, blank=True, null=True)
    denmag = models.IntegerField(blank=True, null=True)
    dosah_ucinku = models.CharField(max_length=20, blank=True, null=True)
    uroven_vyrobce = models.CharField(max_length=10)
    sfera = models.CharField(max_length=20)
    popis = models.TextField()
    pochvez = models.CharField(max_length=1)
    autor = models.CharField(max_length=25, blank=True, null=True)
    autmail = models.CharField(max_length=30, blank=True, null=True)
    zdroj = models.CharField(max_length=100, blank=True, null=True)
    zdrojmail = models.CharField(max_length=40, blank=True, null=True)
    datum = models.DateTimeField()
    schvaleno = models.CharField(max_length=1)
    skupina = models.CharField(max_length=30)
    tisknuto = models.SmallIntegerField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alchpredmety'


class Ankety(models.Model):
    otazka = models.TextField(blank=True, null=True)
    odp1 = models.CharField(max_length=250)
    p1 = models.IntegerField()
    odp2 = models.CharField(max_length=250)
    p2 = models.IntegerField()
    odp3 = models.CharField(max_length=250)
    p3 = models.IntegerField()
    odp4 = models.CharField(max_length=250)
    p4 = models.IntegerField()
    odp5 = models.CharField(max_length=250)
    p5 = models.IntegerField()
    odp6 = models.CharField(max_length=250)
    p6 = models.IntegerField()
    odp7 = models.CharField(max_length=250)
    p7 = models.IntegerField()
    odp8 = models.CharField(max_length=250)
    p8 = models.IntegerField()
    odp9 = models.CharField(max_length=250)
    p9 = models.IntegerField()
    odp10 = models.CharField(max_length=250)
    p10 = models.IntegerField()
    spusteno = models.IntegerField()
    konec = models.IntegerField()
    id_stolu = models.IntegerField()
    jmenovite = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ankety'


class AnketyHlasy(models.Model):
    anketa_id = models.IntegerField()
    user_id = models.IntegerField()
    answer_id = models.IntegerField()
    user_comment = models.CharField(max_length=1023)

    class Meta:
        managed = False
        db_table = 'ankety_hlasy'
        unique_together = (('anketa_id', 'user_id'),)


class BannedIp(models.Model):
    ip = models.CharField(primary_key=True, max_length=16)
    popis = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'banned_ip'


class Chat1Zaloha(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat1_zaloha'


class Chat1Zaloha2(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat1_zaloha2'


class Chat1(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat_1'


class Chat2(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat_2'


class Chat3(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat_3'


class Chat4(models.Model):
    pro = models.IntegerField()
    od = models.IntegerField()
    cas = models.IntegerField()
    zprava = models.TextField()
    nick = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'chat_4'


class ChatAktivni(models.Model):
    nick = models.TextField(blank=True, null=True)
    cas = models.IntegerField(blank=True, null=True)
    mistnost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chat_aktivni'


class ChatMistnosti(models.Model):
    nazev = models.CharField(max_length=40)
    popis = models.CharField(max_length=255)
    stala = models.IntegerField()
    spravce = models.IntegerField()
    septani = models.IntegerField()
    zamknuto = models.IntegerField()
    sprava = models.IntegerField()
    bez_hostu = models.IntegerField()
    duch = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_mistnosti'


class ChatPristupy(models.Model):
    mistnost_id = models.PositiveIntegerField(primary_key=True)
    nick = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'chat_pristupy'
        unique_together = (('mistnost_id', 'nick'),)


class ChatProperties(models.Model):
    id_uz = models.PositiveIntegerField()
    param = models.CharField(max_length=25)
    value = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'chat_properties'


class Diskuze(models.Model):
    id_cizi = models.IntegerField()
    nickname = models.CharField(max_length=25)
    email = models.CharField(max_length=40)
    text = models.TextField()
    datum = models.DateTimeField()
    cizi_tbl = models.CharField(max_length=20)
    reputace = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diskuze'


class DiskuzeMaillist(models.Model):
    id_uz = models.IntegerField(primary_key=True)
    id_cizi = models.IntegerField()
    email = models.CharField(max_length=40)
    cizi_tbl = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'diskuze_maillist'
        unique_together = (('id_uz', 'id_cizi', 'cizi_tbl'),)


class Dobrodruzstvi(models.Model):
    jmeno = models.TextField()
    anotace = models.TextField()
    cesta = models.TextField(blank=True, null=True)
    klicsl = models.TextField()
    pochvez = models.CharField(max_length=1)
    autor = models.TextField(blank=True, null=True)
    autmail = models.TextField(blank=True, null=True)
    datum = models.DateTimeField()
    zdroj = models.TextField(blank=True, null=True)
    zdrojmail = models.TextField(blank=True, null=True)
    schvaleno = models.CharField(max_length=1)
    pocet_hlasujicich = models.IntegerField()
    hodnota_hlasovani = models.IntegerField()
    precteno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dobrodruzstvi'


class Dovednosti(models.Model):
    jmeno = models.TextField()
    vlastnost = models.TextField()
    obtiznost = models.TextField()
    overovani = models.TextField()
    totuspech = models.TextField()
    uspech = models.TextField()
    neuspech = models.TextField()
    fatneuspech = models.TextField()
    popis = models.TextField()
    autor = models.TextField()
    autmail = models.TextField()
    zdroj = models.TextField()
    zdrojmail = models.TextField()
    schvaleno = models.CharField(max_length=1)
    datum = models.DateTimeField()
    tisknuto = models.PositiveIntegerField()
    pochvez = models.CharField(max_length=1)
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)
    hlasoval = models.TextField(blank=True, null=True)
    precteno = models.IntegerField()
    skupina = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'dovednosti'


class Downloady(models.Model):
    jmeno = models.TextField()
    cesta = models.TextField(blank=True, null=True)
    pochvez = models.CharField(max_length=1)
    autor = models.TextField(blank=True, null=True)
    autmail = models.TextField(blank=True, null=True)
    datum = models.DateTimeField()
    zdroj = models.TextField(blank=True, null=True)
    zdrojmail = models.TextField(blank=True, null=True)
    schvaleno = models.CharField(max_length=1)
    format = models.TextField()
    popis = models.TextField()
    velikost = models.IntegerField()
    skupina = models.TextField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'downloady'


class Duchovo(models.Model):
    datum = models.IntegerField()
    param = models.CharField(max_length=15)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'duchovo'


class Duchovo1(models.Model):
    datum = models.IntegerField()
    param = models.CharField(max_length=15)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'duchovo1'


class Forum(models.Model):
    nickname = models.CharField(max_length=64)
    email = models.TextField(blank=True, null=True)
    datum = models.DateTimeField()
    text = models.TextField()
    reg = models.CharField(max_length=50)
    reputace = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'forum'


class Forums(models.Model):
    name = models.CharField(max_length=50)
    active = models.SmallIntegerField()
    description = models.CharField(max_length=255)
    config_suffix = models.CharField(max_length=50)
    folder = models.CharField(max_length=1)
    parent = models.IntegerField()
    display = models.PositiveIntegerField()
    table_name = models.CharField(max_length=50)
    moderation = models.CharField(max_length=1)
    email_list = models.CharField(max_length=50)
    email_return = models.CharField(max_length=50)
    email_tag = models.CharField(max_length=50)
    check_dup = models.PositiveSmallIntegerField()
    multi_level = models.PositiveSmallIntegerField()
    collapse = models.PositiveSmallIntegerField()
    flat = models.PositiveSmallIntegerField()
    lang = models.CharField(max_length=50)
    html = models.CharField(max_length=40)
    table_width = models.CharField(max_length=4)
    table_header_color = models.CharField(max_length=7)
    table_header_font_color = models.CharField(max_length=7)
    table_body_color_1 = models.CharField(max_length=7)
    table_body_color_2 = models.CharField(max_length=7)
    table_body_font_color_1 = models.CharField(max_length=7)
    table_body_font_color_2 = models.CharField(max_length=7)
    nav_color = models.CharField(max_length=7)
    nav_font_color = models.CharField(max_length=7)
    allow_uploads = models.CharField(max_length=1)
    upload_types = models.CharField(max_length=100)
    upload_size = models.PositiveIntegerField()
    max_uploads = models.PositiveIntegerField()
    security = models.PositiveIntegerField()
    showip = models.PositiveSmallIntegerField()
    emailnotification = models.PositiveSmallIntegerField()
    body_color = models.CharField(max_length=7)
    body_link_color = models.CharField(max_length=7)
    body_alink_color = models.CharField(max_length=7)
    body_vlink_color = models.CharField(max_length=7)
    required_level = models.SmallIntegerField()
    permissions = models.SmallIntegerField()
    allow_edit = models.SmallIntegerField()
    allow_langsel = models.SmallIntegerField()
    displayflag = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'forums'


class ForumsAuth(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    webpage = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    icq = models.CharField(max_length=50)
    aol = models.CharField(max_length=50)
    yahoo = models.CharField(max_length=50)
    msn = models.CharField(max_length=50)
    jabber = models.CharField(max_length=50)
    signature = models.CharField(max_length=255)
    max_group_permission_level = models.PositiveIntegerField()
    permission_level = models.PositiveIntegerField()
    hide_email = models.PositiveIntegerField()
    lang = models.CharField(max_length=50)
    password_tmp = models.CharField(max_length=50)
    combined_token = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'forums_auth'


class ForumsForum2Group(models.Model):
    forum_id = models.PositiveIntegerField()
    group_id = models.PositiveIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'forums_forum2group'
        unique_together = (('group_id', 'forum_id'),)


class ForumsGroups(models.Model):
    name = models.CharField(max_length=255)
    permission_level = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'forums_groups'


class ForumsModerators(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    forum_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'forums_moderators'
        unique_together = (('user_id', 'forum_id'),)


class Grouplimits(models.Model):
    id_uz = models.IntegerField()
    max_soukr = models.SmallIntegerField(blank=True, null=True)
    max_verej = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grouplimits'


class Groupmembers(models.Model):
    id_skupiny = models.IntegerField()
    id_uz = models.IntegerField()
    clenstvi = models.IntegerField(blank=True, null=True)
    caszmeny = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupmembers'


class Hranicarkouzla(models.Model):
    jmeno = models.TextField()
    mag = models.SmallIntegerField()
    magpop = models.TextField()
    dosah = models.SmallIntegerField(blank=True, null=True)
    dosahpop = models.TextField(blank=True, null=True)
    rozsah = models.SmallIntegerField(blank=True, null=True)
    rozsahpop = models.TextField(blank=True, null=True)
    vyvolani = models.SmallIntegerField(blank=True, null=True)
    vyvolanipop = models.TextField(blank=True, null=True)
    druh = models.TextField(blank=True, null=True)
    skupina = models.TextField()
    cetnost = models.TextField(blank=True, null=True)
    pomucky = models.TextField(blank=True, null=True)
    autor = models.TextField(blank=True, null=True)
    autmail = models.TextField(blank=True, null=True)
    zdroj = models.TextField(blank=True, null=True)
    zdrojmail = models.TextField(blank=True, null=True)
    schvaleno = models.CharField(max_length=1)
    datum = models.DateTimeField()
    pochvez = models.CharField(max_length=1)
    popis = models.TextField()
    tisknuto = models.IntegerField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hranicarkouzla'


class Inzerce(models.Model):
    sekce = models.CharField(max_length=20)
    jmeno = models.CharField(max_length=30, blank=True, null=True)
    mail = models.CharField(max_length=30, blank=True, null=True)
    telefon = models.CharField(max_length=15, blank=True, null=True)
    mobil = models.CharField(max_length=15, blank=True, null=True)
    okres = models.CharField(max_length=20, blank=True, null=True)
    text = models.TextField()
    datum = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'inzerce'

class Kouzla(models.Model):
    jmeno = models.TextField()
    kouzsl = models.TextField()
    mag = models.SmallIntegerField()
    magpop = models.TextField()
    past = models.TextField(blank=True, null=True)
    dosah = models.IntegerField(blank=True, null=True)
    dosahpop = models.TextField(blank=True, null=True)
    rozsah = models.IntegerField()
    rozsahpop = models.TextField(blank=True, null=True)
    vyvolani = models.IntegerField()
    vyvolanipop = models.TextField()
    trvani = models.IntegerField()
    trvanipop = models.TextField(blank=True, null=True)
    popis = models.TextField()
    skupina = models.TextField()
    pochvez = models.CharField(max_length=1)
    datum = models.DateTimeField()
    autor = models.TextField(blank=True, null=True)
    autmail = models.TextField(blank=True, null=True)
    zdroj = models.TextField(blank=True, null=True)
    zdrojmail = models.TextField(blank=True, null=True)
    schvaleno = models.CharField(max_length=1)
    tisknuto = models.PositiveIntegerField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kouzla'


class Limity(models.Model):
    oprava_hlasovani_po = models.PositiveIntegerField(primary_key=True)
    platnost = models.CharField(max_length=1)
    oprava_hlasovani_pred = models.IntegerField()
    platnost_limitu_pred = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'limity'


class Linky(models.Model):
    nazev = models.TextField()
    adresa = models.TextField()
    popis = models.TextField()
    pochvez = models.CharField(max_length=1)
    schvaleno = models.CharField(max_length=1)
    datum = models.DateTimeField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linky'




class Mailgroups(models.Model):
    verejna = models.CharField(max_length=3)
    nazev_skupiny = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'mailgroups'


class MaillistCeka(models.Model):
    rubrika = models.CharField(max_length=30)
    data = models.TextField()
    dataplain = models.TextField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'maillist_ceka'


class MentatNewbie(models.Model):
    newbie_id = models.IntegerField(primary_key=True)
    mentat_id = models.IntegerField()
    newbie_rate = models.IntegerField()
    mentat_rate = models.IntegerField()
    locked = models.CharField(max_length=2)
    penalty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mentat_newbie'
        unique_together = (('newbie_id', 'mentat_id'),)


class MentatsAvail(models.Model):
    user_id = models.IntegerField(primary_key=True)
    intro_m = models.TextField()
    intro_z = models.TextField()

    class Meta:
        managed = False
        db_table = 'mentats_avail'


class MsDilna(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_dilna'


class MsDilnaAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_dilna_attachments'
        unique_together = (('id', 'message_id'),)


class MsDilnaBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_dilna_bodies'


class MsDracidoupecz(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_dracidoupecz'


class MsDracidoupeczBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_dracidoupecz_bodies'


class MsGalerieDilna(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_galerie_dilna'


class MsGalerieDilnaAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_galerie_dilna_attachments'
        unique_together = (('id', 'message_id'),)


class MsGalerieDilnaBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_galerie_dilna_bodies'


class MsHtmldilna(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_htmldilna'


class MsHtmldilnaAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_htmldilna_attachments'
        unique_together = (('id', 'message_id'),)


class MsHtmldilnaBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_htmldilna_bodies'


class MsOstatni(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_ostatni'


class MsOstatniAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_ostatni_attachments'
        unique_together = (('id', 'message_id'),)


class MsOstatniBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_ostatni_bodies'


class MsPj(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_pj'


class MsPjAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_pj_attachments'
        unique_together = (('id', 'message_id'),)


class MsPjBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_pj_bodies'


class MsPravidla(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_pravidla'


class MsPravidlaAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_pravidla_attachments'
        unique_together = (('id', 'message_id'),)


class MsPravidlaBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_pravidla_bodies'


class MsRing(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_ring'


class MsRingAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_ring_attachments'
        unique_together = (('id', 'message_id'),)


class MsRingBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_ring_bodies'


class MsRoleplaying(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datestamp = models.DateTimeField()
    thread = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    author = models.CharField(max_length=37)
    subject = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    host = models.CharField(max_length=255)
    email_reply = models.CharField(max_length=1)
    approved = models.CharField(max_length=1)
    msgid = models.CharField(max_length=100)
    modifystamp = models.PositiveIntegerField()
    userid = models.PositiveIntegerField()
    closed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ms_roleplaying'


class MsRoleplayingAttachments(models.Model):
    message_id = models.PositiveIntegerField()
    filename = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ms_roleplaying_attachments'
        unique_together = (('id', 'message_id'),)


class MsRoleplayingBodies(models.Model):
    body = models.TextField()
    thread = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'ms_roleplaying_bodies'


class Navstevnost(models.Model):
    ip = models.CharField(primary_key=True, max_length=16)
    naposled = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'navstevnost'


# class Pomocnici(models.Model):
#     id_zaznamu = models.AutoField(unique=True)
#     id_pomocnika = models.PositiveIntegerField()
#     nick_pomocnika = models.CharField(max_length=25)
#     nazev_dila = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'pomocnici'


class Posta(models.Model):
    odesilatel = models.CharField(max_length=25)
    prijemce = models.CharField(max_length=25)
    viditelnost = models.CharField(max_length=1)
    text = models.TextField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'posta'


class Pravomoci(models.Model):
    id_user = models.IntegerField(primary_key=True)
    funkce = models.CharField(max_length=20)
    stupen = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pravomoci'
        unique_together = (('id_user', 'funkce'),)


class Predmety(models.Model):
    jmeno = models.TextField()
    uc = models.TextField(db_column='UC', blank=True, null=True)  # Field name made lowercase.
    kz = models.CharField(db_column='KZ', max_length=3, blank=True, null=True)  # Field name made lowercase.
    delka = models.CharField(max_length=3, blank=True, null=True)
    cena = models.IntegerField()
    popis = models.TextField()
    autor = models.TextField(blank=True, null=True)
    autmail = models.TextField(blank=True, null=True)
    datum = models.DateTimeField()
    pochvez = models.CharField(max_length=1)
    malydostrel = models.IntegerField(blank=True, null=True)
    strednidostrel = models.IntegerField(blank=True, null=True)
    velkydostrel = models.IntegerField(blank=True, null=True)
    sfera = models.IntegerField(blank=True, null=True)
    vaha = models.IntegerField()
    zdroj = models.TextField(blank=True, null=True)
    zdrojmail = models.TextField(blank=True, null=True)
    schvaleno = models.CharField(max_length=1)
    skupina = models.TextField()
    tisknuto = models.SmallIntegerField()
    pocet_hlasujicich = models.IntegerField(blank=True, null=True)
    hodnota_hlasovani = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predmety'

class PsiSmecka(models.Model):
    id_uz = models.IntegerField(primary_key=True)
    cizi_tbl = models.CharField(max_length=20)
    id_dilo = models.IntegerField()
    navstiveno = models.IntegerField()
    neprectenych = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'psi_smecka'
        unique_together = (('id_uz', 'cizi_tbl', 'id_dilo'),)


class PutykaBook(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_uz = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_book'
        unique_together = (('id_stolu', 'id_uz'),)


class PutykaLinky(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_linku = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_linky'
        unique_together = (('id_stolu', 'id_linku'),)


class PutykaNastenky(models.Model):
    id_stolu = models.IntegerField(unique=True)
    nazev_stolu = models.CharField(max_length=128)
    text_nastenky = models.TextField()
    posledni_zmena = models.DateTimeField(blank=True, null=True)
    zmenil = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'putyka_nastenky'


class PutykaNavstevnost(models.Model):
    cas = models.DateTimeField(primary_key=True)
    misto = models.CharField(max_length=31)
    pocet = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_navstevnost'
        unique_together = (('cas', 'misto'),)


class PutykaNeoblibene(models.Model):
    id_uz = models.IntegerField()
    id_stolu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_neoblibene'


class PutykaPrispevky(models.Model):
    id_stolu = models.IntegerField()
    text = models.TextField()
    autor = models.CharField(max_length=30)
    reputace = models.IntegerField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'putyka_prispevky'


class PutykaPristup(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    typ_pristupu = models.CharField(max_length=5)
    nick_usera = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'putyka_pristup'
        unique_together = (('id_stolu', 'typ_pristupu', 'nick_usera'),)


class PutykaSekce(models.Model):
    kod = models.IntegerField()
    poradi = models.IntegerField()
    nazev = models.CharField(max_length=50)
    popis = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'putyka_sekce'


class PutykaSlucovani(models.Model):
    id_ja = models.IntegerField()
    id_on = models.IntegerField()
    zustavam = models.SmallIntegerField()
    oznaceni = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'putyka_slucovani'


class PutykaStoly(models.Model):
    jmeno = models.CharField(unique=True, max_length=255)
    popis = models.CharField(max_length=255)
    vlastnik = models.CharField(max_length=30)
    povol_hodnoceni = models.CharField(max_length=1)
    min_level = models.CharField(max_length=1)
    zalozen = models.DateTimeField()
    verejny = models.CharField(max_length=1)
    celkem = models.IntegerField(blank=True, null=True)
    sekce = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_stoly'


class PutykaUzivatele(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_uzivatele = models.IntegerField()
    oblibenost = models.IntegerField()
    navstiveno = models.DateTimeField(blank=True, null=True)
    neprectenych = models.IntegerField(blank=True, null=True)
    sprava = models.IntegerField()
    pristup = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'putyka_uzivatele'
        unique_together = (('id_stolu', 'id_uzivatele'),)


class ReklamaBanneryZasobnik(models.Model):
    vlastnik = models.IntegerField()
    cesta = models.CharField(max_length=60, blank=True, null=True)
    cislo = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'reklama_bannery_zasobnik'


class ReklamaKampaneBannery(models.Model):
    vlastnik = models.IntegerField()
    cesta = models.CharField(max_length=60)
    odkaz = models.CharField(max_length=60)
    imp_zadane = models.IntegerField()
    imp_zobrazene = models.IntegerField()
    poc_kliku = models.IntegerField()
    zacatek = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reklama_kampane_bannery'


class ReklamaKampaneText(models.Model):
    vlastnik = models.IntegerField()
    text = models.CharField(max_length=255)
    odkaz = models.CharField(max_length=60)
    bezici = models.CharField(max_length=1)
    imp_zadane = models.IntegerField()
    imp_zobrazene = models.IntegerField()
    poc_kliku = models.IntegerField()
    zacatek = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reklama_kampane_text'


class ReklamaMail(models.Model):
    text = models.TextField()
    k_roz = models.PositiveIntegerField()
    rozeslano = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'reklama_mail'


class ReklamaUkoncene(models.Model):
    vlastnik = models.IntegerField()
    imp_zobrazene = models.IntegerField()
    poc_kliku = models.IntegerField()
    zacatek = models.DateTimeField()
    konec = models.DateTimeField()
    typ = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'reklama_ukoncene'


class ReklamaUsers(models.Model):
    loginname = models.CharField(max_length=30)
    heslo = models.CharField(max_length=35)
    email = models.CharField(max_length=30)
    imprese_ban = models.IntegerField()
    imprese_txt = models.IntegerField()
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reklama_users'


class ReputaceLog(models.Model):
    id_zaznamu = models.AutoField(primary_key=True)
    dal = models.CharField(max_length=30)
    prijal = models.CharField(max_length=30)
    akce = models.CharField(max_length=3)
    v_diskusi = models.CharField(max_length=1, blank=True, null=True)
    id_prispevku = models.PositiveIntegerField(blank=True, null=True)
    date = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'reputace_log'


class ReputaceSpecial(models.Model):
    prijal_nick = models.CharField(max_length=25)
    duvod_udeleni = models.CharField(max_length=200)
    hodnota = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'reputace_special'


class RubrikyPristup(models.Model):
    id_usr = models.PositiveIntegerField(primary_key=True)
    id_cizi = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rubriky_pristup'
        unique_together = (('id_usr', 'id_cizi', 'rubrika'),)


class Runy(models.Model):
    id_darce = models.IntegerField()
    nick_darce = models.CharField(max_length=30)
    id_prijemce = models.IntegerField(blank=True, null=True)
    nick_prijemce = models.CharField(max_length=30)
    typ = models.CharField(max_length=15)
    grafika = models.SmallIntegerField()
    venovani = models.TextField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'runy'


class Skiny(models.Model):
    nazev = models.CharField(max_length=10)
    jmeno = models.CharField(max_length=50)
    autor = models.CharField(max_length=20)
    autmail = models.CharField(max_length=40)
    popis = models.TextField()

    class Meta:
        managed = False
        db_table = 'skiny'


class Slovnicek(models.Model):
    jazyk = models.IntegerField()
    kat = models.CharField(max_length=33)
    cis = models.CharField(max_length=7)
    rod = models.CharField(max_length=9)
    spc1 = models.SmallIntegerField()
    spc2 = models.SmallIntegerField()
    text = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'slovnicek'


class SortPrim(models.Model):
    autor = models.CharField(primary_key=True, max_length=30)
    prumer = models.CharField(max_length=3)
    pocet_prispevku = models.IntegerField()
    pocet_v_diskuzi = models.IntegerField()
    reputace = models.IntegerField()
    level = models.CharField(max_length=1)
    level_new = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'sort_prim'


class Spravci(models.Model):
    loginname = models.CharField(max_length=200)
    pass_field = models.CharField(db_column='pass', max_length=32)  # Field renamed because it was a Python reserved word.
    rubaktuality = models.CharField(max_length=1)
    hrbitov = models.CharField(max_length=1)
    rubdobrodruzstvi = models.CharField(max_length=1)
    rubclanky = models.CharField(max_length=1)
    rublinky = models.CharField(max_length=1)
    rubbestiar = models.CharField(max_length=1)
    rubvalecnik = models.CharField(max_length=1)
    rubhranicar = models.CharField(max_length=1)
    rubalchymista = models.CharField(max_length=1)
    rubkouzelnik = models.CharField(max_length=1)
    rubzlodej = models.CharField(max_length=1)
    rubnovapovolani = models.CharField(max_length=1)
    mail = models.CharField(max_length=255)
    rubpredmety = models.CharField(max_length=1)
    rubdownloady = models.CharField(max_length=1)
    rubgalerie = models.CharField(max_length=1)
    rubdovednosti = models.CharField(max_length=1)
    rubnoverasy = models.CharField(max_length=1)
    uzivatele = models.CharField(max_length=1)
    rubexpanze = models.CharField(max_length=1)
    alchpred = models.CharField(max_length=1)
    hrankouzla = models.CharField(max_length=1)
    kkouzla = models.CharField(max_length=1)
    rubputyka = models.CharField(max_length=1)
    rubprogram = models.CharField(max_length=1)
    rubms = models.CharField(db_column='rubMS', max_length=1)  # Field name made lowercase.
    rubfotogalerie = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'spravci'


class StatistikyAutori(models.Model):
    autor = models.CharField(primary_key=True, max_length=25)
    rubrika = models.CharField(max_length=25)
    pocet = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistiky_autori'
        unique_together = (('autor', 'rubrika'),)


class StatistikyDila(models.Model):
    autor = models.CharField(max_length=32)
    rubrika = models.CharField(max_length=32)
    skupina = models.CharField(max_length=32)
    hodnoceni = models.FloatField()
    datum = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'statistiky_dila'


# class Temptable(models.Model):
#     id = models.PositiveIntegerField()
#     id_cizi = models.PositiveIntegerField()
#     rubrika = models.CharField(max_length=20, blank=True, null=True)
#     pochvez = models.PositiveIntegerField()

#     class Meta:
#         managed = False
#         db_table = 'temptable'


class UserRatings(models.Model):
    record_id = models.AutoField(primary_key=True)
    rating_time = models.IntegerField()
    byfk = models.IntegerField(db_column='byFK')  # Field name made lowercase.
    forfk = models.IntegerField(db_column='forFK')  # Field name made lowercase.
    visible = models.SmallIntegerField()
    rating_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_ratings'
        unique_together = (('byfk', 'forfk'),)


class UserStats(models.Model):
    user_id = models.IntegerField(primary_key=True)
    loghistory = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'user_stats'


class UzivateleCekajici(models.Model):
    id_zaznamu = models.AutoField(primary_key=True)
    nick_uzivatele = models.CharField(unique=True, max_length=30)
    email = models.CharField(unique=True, max_length=40)
    jmeno = models.CharField(max_length=40)
    prijmeni = models.CharField(max_length=40)
    pohlavi = models.CharField(max_length=4)
    datum = models.IntegerField()
    patron = models.IntegerField()
    primluvy = models.IntegerField()
    osloveni = models.CharField(max_length=50, blank=True, null=True)
    popis_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'uzivatele_cekajici'
        unique_together = (('jmeno', 'prijmeni'),)


class UzivateleFiltry(models.Model):
    id_uz = models.IntegerField(primary_key=True)
    rubrika = models.CharField(max_length=20)
    filtr = models.CharField(max_length=15)
    hodnota = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'uzivatele_filtry'
        unique_together = (('id_uz', 'rubrika', 'filtr'),)


class UzivateleMaillist(models.Model):
    id_uz = models.IntegerField(primary_key=True)
    rubrika = models.CharField(max_length=20)
    email_uz = models.CharField(max_length=40)
    mime = models.CharField(db_column='MIME', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'uzivatele_maillist'
        unique_together = (('id_uz', 'rubrika'),)


class UzivateleZamitnuti(models.Model):
    nick_uzivatele = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    jmeno = models.CharField(max_length=40)
    prijmeni = models.CharField(max_length=40)
    pohlavi = models.CharField(max_length=4)
    datum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uzivatele_zamitnuti'


class ZldHlasovani(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)
    rocnik = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'zld_hlasovani'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika', 'rocnik'), ('id_usr', 'id_prispevku', 'rubrika', 'rocnik'),)


class ZldMain(models.Model):
    rocnik = models.CharField(unique=True, max_length=6)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'zld_main'


class ZldNominace(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    rocnik = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'zld_nominace'


class ZldNominace20012(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2001_2'


class ZldNominace20012Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2001_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20021(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2002_1'


class ZldNominace20021Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2002_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20022(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2002_2'


class ZldNominace20022Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2002_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20031(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2003_1'


class ZldNominace20031Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2003_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20032(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2003_2'


class ZldNominace20032Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2003_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20041(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2004_1'


class ZldNominace20041Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2004_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20042(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2004_2'


class ZldNominace20042Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2004_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20051(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2005_1'


class ZldNominace20051Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2005_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20052(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2005_2'


class ZldNominace20052Hlasoval(models.Model):
    id_usr = models.IntegerField()
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2005_2_hlasoval'
        unique_together = (('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20061(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2006_1'


class ZldNominace20061Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2006_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20062(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2006_2'


class ZldNominace20062Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2006_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20071(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2007_1'


class ZldNominace20071Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2007_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20072(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2007_2'


class ZldNominace20072Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2007_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20081(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2008_1'


class ZldNominace20081Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2008_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20082(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2008_2'


class ZldNominace20082Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2008_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20091(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2009_1'


class ZldNominace20091Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2009_1_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldNominace20092(models.Model):
    cizi_id = models.IntegerField()
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2009_2'


class ZldNominace20092Hlasoval(models.Model):
    id_usr = models.IntegerField(primary_key=True)
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'zld_nominace_2009_2_hlasoval'
        unique_together = (('id_usr', 'pocet_bodu', 'rubrika'), ('id_usr', 'id_prispevku', 'rubrika'),)


class ZldPocitam20012(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2001_2'


class ZldPocitam20021(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2002_1'


class ZldPocitam20022(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2002_2'


class ZldPocitam20031(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2003_1'


class ZldPocitam20032(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2003_2'


class ZldPocitam20041(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2004_1'


class ZldPocitam20042(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2004_2'


class ZldPocitam20051(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2005_1'


class ZldPocitam20052(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2005_2'


class ZldPocitam20061(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2006_1'


class ZldPocitam20062(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2006_2'


class ZldPocitam20071(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2007_1'


class ZldPocitam20072(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2007_2'


class ZldPocitam20081(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2008_1'


class ZldPocitam20082(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2008_2'


class ZldPocitam20091(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2009_1'


class ZldPocitam20092(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2009_2'


class ZldPocitam2010(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2010'


class ZldPocitam2011(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2011'


class ZldPocitam2012(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2012'


class ZldPocitam2013(models.Model):
    id_prispevku = models.IntegerField()
    rubrika = models.CharField(max_length=30)
    pocet_bodu = models.IntegerField()
    misto1 = models.IntegerField()
    misto2 = models.IntegerField()
    misto3 = models.IntegerField()
    cernyd = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zld_pocitam_2013'


class ZldVitezove(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)
    rocnik = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'zld_vitezove'
        unique_together = (('cizi_id', 'rubrika', 'rocnik'),)


class ZldVitezove20012(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2001_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20021(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2002_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20022(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2002_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20031(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2003_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20032(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2003_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20041(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2004_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20042(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2004_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20051(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2005_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20052(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2005_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20061(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2006_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20062(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2006_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20071(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2007_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20072(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2007_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20081(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2008_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20082(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2008_2'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20091(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2009_1'
        unique_together = (('cizi_id', 'rubrika'),)


class ZldVitezove20092(models.Model):
    cizi_id = models.IntegerField(primary_key=True)
    jmeno = models.CharField(max_length=255)
    rubrika = models.CharField(max_length=30)
    autor = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'zld_vitezove_2009_2'
        unique_together = (('cizi_id', 'rubrika'),)
