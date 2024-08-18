from ddcz.forms.signup import SignUpForm
from ddcz.models import UserProfile

from django.test import TestCase


class TestSignupForm(TestCase):
    def test_duplicate_nick_registrations(self):
        test_nick = "testnick"
        UserProfile.objects.create(nick=test_nick)

        form = SignUpForm(
            {
                "nick": test_nick,
                "email": "yolo@example.com",
                "name_given": "John",
                "name_family": "Doe",
                "salutation": "Dr(ak).",
                "password": "password",
                "password_confirm": "password",
                "gdpr": "T",
                "gender": "F",
                "age": 20,
            }
        )
        self.assertFalse(form.is_valid())

    def test_duplicate_email_registrations(self):
        test_email = "testingemail@example.com"
        UserProfile.objects.create(nick="testnick", email=test_email)

        form = SignUpForm(
            {
                "nick": "whatever",
                "email": test_email,
                "name_given": "John",
                "name_family": "Doe",
                "salutation": "Dr(ak).",
                "password": "password",
                "password_confirm": "password",
                "gdpr": "T",
                "gender": "F",
                "age": 20,
            }
        )
        self.assertFalse(form.is_valid())
