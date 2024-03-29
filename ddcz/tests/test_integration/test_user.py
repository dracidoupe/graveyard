from django.test import Client, TestCase

from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User

from ddcz.models import UserProfile

from ..model_generator import get_alphabetic_user_profiles


class PasswordResetTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

        self.valid_password = "c1QoUGFss5K6ozi"
        self.valid_email = "test@example.com"
        self.nick = "integration test user"

        self.valid_user = User.objects.create_user(
            username=self.nick, password=self.valid_password
        )

        self.valid_profile = UserProfile.objects.create(
            nick=self.nick,
            email=self.valid_email,
            user=self.valid_user,
        )

    def test_sending_form(self):
        self.assertEqual(len(mail.outbox), 0)

        res = self.client.post(
            reverse("ddcz:password-reset"), {"email": self.valid_email}
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEquals(302, res.status_code)


class UserListTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

        self.users = get_alphabetic_user_profiles(
            number_of_users=3, saved=True, nick_prefix="generated-user"
        )

    def test_users_displayed(self):
        response = self.client.get("/uzivatele/")
        for user in self.users:
            self.assertContains(response, user.nick)
