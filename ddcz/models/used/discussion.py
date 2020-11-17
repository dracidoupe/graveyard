from django.db import models

from ..magic import MisencodedCharField, MisencodedTextField

class Phorum(models.Model):
    nickname = MisencodedCharField(max_length=64)
    email = MisencodedTextField(blank=True, null=True)
    datum = models.DateTimeField(auto_now_add=True)
    text = MisencodedTextField()
    # stands for 'registered', contains either '1' or IP address
    reg = MisencodedCharField(max_length=50)
    reputace = models.IntegerField()

    class Meta:
        db_table = 'forum'
