from django.test import Client, TestCase

from django.urls import reverse
from django.contrib.auth.models import User

from ddcz.models import UserProfile

class PasswordResetTestCase(TestCase):
    fixtures = ['pages']

    def setUp(self):
        super().setUp()
        self.client = Client()

        self.valid_password = 'xoxo'
        self.valid_email = 'test@example.com'
        self.nick = 'integration test user'

        self.valid_user = User.objects.create(
            username = self.nick,
            password = self.valid_password
        )

        self.valid_profile = UserProfile.objects.create(
            nick_uzivatele = self.nick,
            email_uzivatele = self.valid_email,
            user = self.valid_user
        )


    def test_sending_form(self):
        res = self.client.post(reverse('ddcz:password-reset'), {
            'email': self.valid_email
        })

        self.assertEquals(302, res.status_code)