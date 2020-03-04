from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from ...text import create_slug
from ..magic import MisencodedCharField, MisencodedTextField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    jmeno_uzivatele = MisencodedCharField(max_length=20)
    nick_uzivatele = MisencodedCharField(unique=True, max_length=25)
    prijmeni_uzivatele = MisencodedCharField(max_length=20)
    psw_uzivatele = MisencodedCharField(max_length=40)
    email_uzivatele = MisencodedCharField(max_length=50)
    pohlavi_uzivatele = MisencodedCharField(max_length=4, blank=True, null=True)
    vek_uzivatele = models.IntegerField(default=0)
    kraj_uzivatele = MisencodedCharField(max_length=20)
    chat_barva = MisencodedCharField(max_length=6)
    chat_pismo = models.IntegerField(default=12)
    chat_reload = models.IntegerField(default=15)
    chat_zprav = models.IntegerField(default=20)
    chat_filtr = MisencodedCharField(max_length=255, blank=True, null=True)
    chat_filtr_zobrazit = models.IntegerField(default=0)
    pospristup = models.DateTimeField(auto_now_add=True)
    level = MisencodedCharField(max_length=1)
    icq_uzivatele = models.IntegerField(default=0)
    vypsat_udaje = MisencodedCharField(max_length=15)
    ikonka_uzivatele = MisencodedCharField(max_length=25, blank=True, null=True)
    popis_uzivatele = MisencodedCharField(max_length=255, blank=True, null=True)
    nova_posta = models.IntegerField(default=0)
    skin = MisencodedCharField(max_length=10)
    reputace = models.IntegerField(default=0)
    reputace_rozdel = models.PositiveIntegerField(default=0)
    status = MisencodedCharField(max_length=1)
    reg_schval_datum = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    indexhodnotitele = models.DecimalField(max_digits=4, decimal_places=2, default=-99.99)
    reload = MisencodedCharField(max_length=1)
    max_level = models.IntegerField(blank=True, null=True)
    api_key = MisencodedCharField(unique=True, max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'uzivatele'

    def get_slug(self):
        slug = create_slug(self.nick_uzivatele)
        if not slug:
            slug = 'neznamy'
            #TODO: log an error
        return slug

    def get_icon_url(self):
        if not self.ikonka_uzivatele:
            return None
        else:
            return urljoin(
                settings.USER_ICON_MEDIA_ROOT_URL,
                self.ikonka_uzivatele
            )

    icon_url = property(get_icon_url)
    slug = property(get_slug)



User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Note that unlike the normal model, we are creating the User lazily
    # (instead of UserProfile as usual). Hence, on creation, UserProfile is assumed
    # to exist (and needs to be updated with proper relation manually), whereas
    # afterwards profiles can be updated as usual
    if created:
        # YOU are responsible for properly linking User and UserProfile
        # outside of signal handling!
        # ALWAYS use .users.create_user
        pass
    else:
        instance.profile.save()



class LevelSystemParams(models.Model):
    parametr = MisencodedCharField(primary_key=True, max_length=40)
    hodnota = MisencodedCharField(max_length=30)

    class Meta:
        db_table = 'level_parametry_2'
