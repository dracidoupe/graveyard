from django.db import models
from django.db.models import Q
from django.urls import reverse

from ..magic import MisencodedCharField, MisencodedTextField
from .users import UserProfile
from .creations import CreativePage

ADD_PHORUM_COMMENT = "a"
DELETE_PHORUM_COMMENT = "d"
CREATION_COMMENT_PAGE_SIZE = 10


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

    def get_absolute_url(self):
        return reverse("ddcz:phorum-item", kwargs={"comment_id": self.pk})

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
    reputation = models.IntegerField(db_column="reputace", default=0)
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

    def __str__(self):
        return f"{self.nickname} v {self.foreign_table}"

    def get_url_for_page(self, page):
        model = CreativePage.get_model_from_slug(self.foreign_table)
        creation = getattr(self, "creation", None) or model.objects.get(
            id=self.foreign_id
        )
        url = reverse(
            "ddcz:creation-detail",
            kwargs={
                "creative_page_slug": self.foreign_table,
                "creation_id": creation.id,
                "creation_slug": creation.get_slug(),
            },
        )
        page_query = f"?z_s={page}" if page > 1 else ""
        return f"{url}{page_query}#comment-{self.pk}"

    def get_absolute_url(self):
        newer_comments = CreationComment.objects.filter(
            Q(date__gt=self.date) | Q(date=self.date, pk__gt=self.pk),
            foreign_table=self.foreign_table,
            foreign_id=self.foreign_id,
        ).count()
        page = newer_comments // CREATION_COMMENT_PAGE_SIZE + 1
        return self.get_url_for_page(page)


class Letter(models.Model):
    # TODO: Migrate those to have a profile_id relation, same as with Phorum posts etc.
    sender = MisencodedCharField(max_length=25, db_column="odesilatel")
    receiver = MisencodedCharField(max_length=25, db_column="prijemce")
    # TODO: Make this enum for readability
    # 3 = visible for both
    # 2 = visible for receiver only
    # 1 = visible for sender only
    # 0 = deleted by both, should be pruned
    visibility = models.CharField(max_length=1, db_column="viditelnost")
    text = MisencodedTextField()
    date = models.DateTimeField(db_column="datum")

    class Meta:
        db_table = "posta"
