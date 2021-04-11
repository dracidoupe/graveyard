from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField
from .users import UserProfile


class Phorum(models.Model):
    nickname = MisencodedCharField(max_length=64)
    email = MisencodedTextField(blank=True, null=True)
    datum = models.DateTimeField(auto_now_add=True)
    text = MisencodedTextField()
    # stands for 'registered', contains either '1' or IP address
    reg = MisencodedCharField(max_length=50)
    reputace = models.IntegerField()
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        db_table = "forum"

    @property
    def user_profile_url(self):
        if self.user:
            return self.user.profile_url
        else:
            return None

    @property
    def by_registered_user(self):
        return self.reg == "1" and self.user


class CreationComment(models.Model):
    nickname = MisencodedCharField(max_length=25)
    email = MisencodedCharField(max_length=40)
    text = MisencodedTextField()
    datum = models.DateTimeField(auto_now_add=True)
    reputace = models.IntegerField()
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, blank=True, null=True
    )

    # This is taken from the previous version. In order to minimize the amount of migrations,
    # it's used as it is. Once the old version is done, the `cizi_tbl` (Foreign Table) should
    # be replaced with model name and the whole model should be migrated to GenericForeignKey, see
    # https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations and
    # https://github.com/dracidoupe/graveyard/issues/165

    # Refactor is needed. `cizi_tbl` gives an illusion to refer to a model, but no, it refers
    # to a CreativePage slug instead
    cizi_tbl = MisencodedCharField(max_length=20)
    id_cizi = models.IntegerField()

    class Meta:
        db_table = "diskuze"
