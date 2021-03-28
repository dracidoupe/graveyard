from django.test import Client, TestCase
from django.contrib.auth.models import User

from ddcz.models import Phorum, UserProfile


class PhorumCommentTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.message = "Ahojky, já jsem Ignác Zlosynus"
        self.message2 = "Slyším tě, pozemšťane!"
        self.nickname = "neelegant"
        self.nickname2 = "astralniucho"

        self.valid_user = User.objects.create_user(
            username=self.nickname, password="bobr-evropsky"
        )

        self.valid_user2 = User.objects.create_user(
            username=self.nickname2, password="vydra-ricni"
        )

        self.user_profile = UserProfile.objects.create(
            nick_uzivatele=self.nickname,
            email_uzivatele="physics@example.com",
            user=self.valid_user,
        )

        self.user_profile2 = UserProfile.objects.create(
            nick_uzivatele=self.nickname2,
            email_uzivatele="mathematics@example.com",
            user=self.valid_user2,
        )

        self.comment = Phorum.objects.create(
            reputace=0,
            reg=1,
            text=self.message,
            nickname=self.nickname,
            email="physics@example.com",
            user=self.user_profile,
        )

        self.comment2 = Phorum.objects.create(
            reputace=0,
            reg=1,
            text=self.message2,
            nickname=self.nickname2,
            email="mathematics@example.com",
            user=self.user_profile2,
        )

    def test_comment_present(self):
        res = self.client.get("/forum/")
        self.assertInHTML(self.message, res.content.decode("utf-8"))
        self.assertInHTML(self.message2, res.content.decode("utf-8"))

    def test_add_comment(self):
        self.client.force_login(user=self.valid_user)
        message = "Na Moravě krásně je, když jsou v Praze závěje."
        res = self.client.post(
            "/forum/",
            {"text": message, "post_type": "a", "submit": "Přidej"},
            follow=True,
        )
        self.assertEquals(200, res.status_code)
        self.assertInHTML(message, res.content.decode("utf-8"))

    def test_delete_comment(self):
        self.client.force_login(user=self.valid_user)
        post_id = self.comment.id
        html = self.client.get("/forum/").content.decode("utf-8")
        res = self.client.post(
            "/forum/",
            {"post_id": post_id, "post_type": "d", "submit": "Smazat"},
            follow=True,
        )
        self.assertHTMLNotEqual(html, res.content.decode("utf-8"))

    def test_no_delete_comment(self):
        self.client.force_login(user=self.valid_user)
        post_id = self.comment2.id
        res = self.client.post(
            "/forum/",
            {"post_id": post_id, "post_type": "d", "submit": "Smazat"},
            follow=True,
        )
        html = res.content.decode("utf-8")
        self.assertInHTML(self.message2, html)
        self.assertInHTML("Zprávu se nepodařilo smazat.", html)
