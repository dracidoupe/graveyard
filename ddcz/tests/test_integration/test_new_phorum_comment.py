from django.test import Client, TestCase
from django.contrib.auth.models import User

from ddcz.models import Phorum, UserProfile


class PhorumCommentTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.message = "Ahojky, já jsem Ignác Zlosynus"
        self.nickname = "Neelegant"

        self.comment = Phorum.objects.create(
            reputace=0,
            reg=1,
            text=self.message,
            nickname=self.nickname,
            email="jaraduuuuu@example.com",
        )

        self.valid_user = User.objects.create_user(
            username=self.nickname, password='almad'
        )

        self.user = UserProfile.objects.create(
            nick_uzivatele=self.nickname,
            email_uzivatele="alcator@example.com",
            user=self.valid_user,
        )

    def test_comment_present(self):
        res = self.client.get("/forum")
        self.assertInHTML(self.message, res.content.decode("utf-8"))

    def test_add_comment(self):
        message = "Moje"
        self.client.force_login(user=self.valid_user)        
        res = self.client.post("/forum", {"id_text": message}, follow=True)        
        self.assertEquals(200, res.status_code)
        self.assertInHTML(message, res.content.decode("utf-8"))
