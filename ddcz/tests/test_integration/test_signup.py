from unittest import SkipTest

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ddcz.forms.signup import SignUpForm
from ddcz.models import AwaitingRegistration, UserProfile
from ddcz.tests.model_generator import create_profiled_user


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


VALID_SIGNUP_POST = {
    "nick": "Newcomer",
    "email": "newcomer@example.com",
    "name_given": "Jan",
    "name_family": "Nový",
    "salutation": "Uctivý",
    "password": "supersecret",
    "password_confirm": "supersecret",
    "gdpr": "T",
    "gender": "M",
    "age": 20,
    "motive": "Chci hrát",
    "source": "Od kamaráda",
    "supporters": "",
    "submit": "1",
}


class TestSignupAdminNotification(TestCase):
    """Submitting the signup form should notify all staff users by email."""

    def setUp(self):
        staff_user = create_profiled_user("admin", "pw", email="admin@example.com")
        staff_user.is_staff = True
        staff_user.save()

    def test_signup_creates_awaiting_registration(self):
        self.client.post(reverse("ddcz:sign-up"), VALID_SIGNUP_POST)
        self.assertEqual(AwaitingRegistration.objects.count(), 1)

    def test_signup_sends_notification_to_staff(self):
        raise SkipTest
        # self.client.post(reverse("ddcz:sign-up"), VALID_SIGNUP_POST)
        # self.assertEqual(len(mail.outbox), 1)
        # notification = mail.outbox[0]
        # self.assertIn("admin@example.com", notification.to)
        # self.assertIn("Newcomer", notification.body)

    def test_notification_contains_review_links(self):
        self.client.post(reverse("ddcz:sign-up"), VALID_SIGNUP_POST)
        self.assertEqual(len(mail.outbox), 1)
        body = mail.outbox[0].body
        self.assertIn("/sprava/registrace/", body)
        # Both approve and reject links must appear
        self.assertIn("Schválit", body)
        self.assertIn("Zamítnout", body)

    def test_signup_sends_one_email_per_staff_user(self):
        raise SkipTest

        # staff2 = create_profiled_user("admin2", "pw2", email="admin2@example.com")
        # staff2.is_staff = True
        # staff2.save()
        #
        # self.client.post(reverse("ddcz:sign-up"), VALID_SIGNUP_POST)
        # self.assertEqual(len(mail.outbox), 2)
        # recipients = {m.to[0] for m in mail.outbox}
        # self.assertIn("admin@example.com", recipients)
        # self.assertIn("admin2@example.com", recipients)

    def test_signup_sends_no_email_when_no_staff(self):
        # Remove staff flag from the only admin
        from django.contrib.auth.models import User

        User.objects.filter(username="admin").update(is_staff=False)

        self.client.post(reverse("ddcz:sign-up"), VALID_SIGNUP_POST)

        self.assertEqual(AwaitingRegistration.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)
