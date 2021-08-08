from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField
from .users import UserProfile

ADD_PHORUM_COMMENT = "a"
DELETE_PHORUM_COMMENT = "d"


class Phorum(models.Model):
    nickname = MisencodedCharField(max_length=64, db_column="nickname")
    email = MisencodedTextField(blank=True, null=True, db_column="email")
    date = models.DateTimeField(auto_now_add=True, db_column="datum")
    text = MisencodedTextField(db_column="")
    # stands for 'registered', contains either '1' or IP address
    registered_or_ip = MisencodedCharField(max_length=50, db_column="reg")
    reputation = models.IntegerField(db_column="reputace")
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
        return self.registered_or_ip == "1" and self.user


class CreationComment(models.Model):
    nickname = MisencodedCharField(max_length=25, db_column="nickname")
    email = MisencodedCharField(max_length=40, db_column="email")
    text = MisencodedTextField(db_column="text")
    date = models.DateTimeField(auto_now_add=True, db_column="datum")
    reputation = models.IntegerField(db_column="reputace")
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
    foreign_table = MisencodedCharField(max_length=20, db_column="cizi_tbl")
    foreign_id = models.IntegerField(db_column="id_cizi")

    class Meta:
        db_table = "diskuze"


class Letters(models.Model):
    sender = models.CharField(max_length=25, db_column="odesilatel")
    receiver = models.CharField(max_length=25, db_column="prijemce")
    visibility = models.CharField(max_length=1, db_column="viditelnost")
    text = models.TextField()
    date = models.DateTimeField(db_column="datum")

    class Meta:
        db_table = "posta"
