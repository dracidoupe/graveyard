from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField
from .users import UserProfile

from pprint import pprint


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

    def createNewCommentFromForm(self, form, user, reputation=0):
        self.nickname = user.nick_uzivatele
        self.email = user.email_uzivatele
        self.text = form.cleaned_data["text"]
        self.reg = 1
        self.reputace = reputation
        self.user = user
        self.save()

    def deleteComment(self, comment_id):
        if self.canBeDeleted(comment_id):
            self.objects.get(id=comment_id).delete()

    def canBeDeleted(self, comment_id):
        obj = self.objects.get(id=comment_id)
        if obj.nickname == request.user:
            return obj
        return False
