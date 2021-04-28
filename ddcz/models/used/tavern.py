from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField


class PutykaBook(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_uz = models.IntegerField()

    class Meta:
        db_table = "putyka_book"
        unique_together = (("id_stolu", "id_uz"),)


class PutykaLinky(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_linku = models.IntegerField()

    class Meta:
        db_table = "putyka_linky"
        unique_together = (("id_stolu", "id_linku"),)


class PutykaNastenky(models.Model):
    id_stolu = models.IntegerField(unique=True)
    nazev_stolu = MisencodedCharField(max_length=128)
    text_nastenky = MisencodedTextField()
    posledni_zmena = models.DateTimeField(blank=True, null=True)
    zmenil = MisencodedCharField(max_length=25)

    class Meta:
        db_table = "putyka_nastenky"


class PutykaNavstevnost(models.Model):
    cas = models.DateTimeField(primary_key=True)
    misto = MisencodedCharField(max_length=31)
    pocet = models.IntegerField()

    class Meta:
        db_table = "putyka_navstevnost"
        unique_together = (("cas", "misto"),)


class PutykaNeoblibene(models.Model):
    id_uz = models.IntegerField()
    id_stolu = models.IntegerField()

    class Meta:
        managed = False
        db_table = "putyka_neoblibene"


class PutykaPrispevky(models.Model):
    id_stolu = models.IntegerField()
    text = MisencodedTextField()
    autor = MisencodedCharField(max_length=30)
    reputace = models.IntegerField()
    datum = models.DateTimeField()

    class Meta:
        db_table = "putyka_prispevky"


class PutykaPristup(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    typ_pristupu = MisencodedCharField(max_length=5)
    nick_usera = MisencodedCharField(max_length=30)

    class Meta:
        db_table = "putyka_pristup"
        unique_together = (("id_stolu", "typ_pristupu", "nick_usera"),)


class PutykaSekce(models.Model):
    kod = models.IntegerField()
    poradi = models.IntegerField()
    nazev = MisencodedCharField(max_length=50)
    popis = MisencodedCharField(max_length=255)

    class Meta:
        db_table = "putyka_sekce"


class PutykaSlucovani(models.Model):
    id_ja = models.IntegerField()
    id_on = models.IntegerField()
    zustavam = models.SmallIntegerField()
    oznaceni = MisencodedCharField(max_length=60)

    class Meta:
        db_table = "putyka_slucovani"


class PutykaStoly(models.Model):
    jmeno = MisencodedCharField(unique=True, max_length=255)
    popis = MisencodedCharField(max_length=255)
    vlastnik = MisencodedCharField(max_length=30)
    povol_hodnoceni = MisencodedCharField(max_length=1)
    min_level = MisencodedCharField(max_length=1)
    zalozen = models.DateTimeField()
    verejny = MisencodedCharField(max_length=1)
    celkem = models.IntegerField(blank=True, null=True)
    sekce = models.IntegerField()

    class Meta:
        db_table = "putyka_stoly"


class PutykaUzivatele(models.Model):
    id_stolu = models.IntegerField(primary_key=True)
    id_uzivatele = models.IntegerField()
    oblibenost = models.IntegerField()
    navstiveno = models.DateTimeField(blank=True, null=True)
    neprectenych = models.IntegerField(blank=True, null=True)
    sprava = models.IntegerField()
    pristup = models.IntegerField()

    class Meta:
        db_table = "putyka_uzivatele"
        unique_together = (("id_stolu", "id_uzivatele"),)
