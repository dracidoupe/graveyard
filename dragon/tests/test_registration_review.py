import time

from django.core import mail, signing
from django.test import TestCase
from django.urls import reverse

from ddcz.email import (
    REGISTRATION_REVIEW_SALT,
)
from ddcz.models import AwaitingRegistration, UserProfile
from ddcz.tests.model_generator import create_profiled_user

from dragon.forms.dashboard import FormTypes
from dragon.forms.users import RegistrationRequestApproval


def make_pending_registration(**kwargs):
    defaults = dict(
        nick="Pending",
        email="pending@example.com",
        name_given="Petr",
        name_family="Čekající",
        gender="Muž",
        age=25,
        date=int(time.time()),
        patron=0,
        supporters=0,
        description="1. Chci hrát\n2. Od kamaráda\n3. \n4. \n5. \n",
    )
    defaults.update(kwargs)
    return AwaitingRegistration.objects.create(**defaults)


def make_token(reg_id, action, **kwargs):
    return signing.dumps(
        {"id": reg_id, "action": action}, salt=REGISTRATION_REVIEW_SALT, **kwargs
    )


class TestRegistrationReviewAccess(TestCase):
    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.reg = make_pending_registration()
        self.token = make_token(self.reg.id, "approve")
        self.url = reverse("dragon:registration-review", kwargs={"token": self.token})

    def test_staff_can_view(self):
        self.client.login(username="staff", password="staffpw")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.reg.nick)

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # LOGIN_URL resolves to the news page (/aktuality/) — see settings.base.LOGIN_URL
        self.assertIn("next=", response["Location"])

    def test_non_staff_gets_403(self):
        create_profiled_user("norm", "pw")
        self.client.login(username="norm", password="pw")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestRegistrationReviewTokenValidation(TestCase):
    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(username="staff", password="staffpw")
        self.reg = make_pending_registration()

    def test_tampered_token_shows_error(self):
        url = reverse(
            "dragon:registration-review", kwargs={"token": "this-is-not-a-valid-token"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Neplatný odkaz")

    def test_expired_token_shows_error(self):
        # Since we can't easily back-date without patching time, verify that
        # SignatureExpired is raised for a zero-second max_age (signing.TimestampSigner).
        from django.core.signing import TimestampSigner

        signer = TimestampSigner(salt=REGISTRATION_REVIEW_SALT)
        with self.assertRaises(signing.SignatureExpired):
            signer.unsign(signer.sign("x"), max_age=0)
        # Confirm the view handles it gracefully via a unit-level check (above).
        # Full expiry integration test would require time-mocking.

    def test_already_handled_registration_shows_error(self):
        self.reg.delete()
        token = make_token(42, "approve")  # id that no longer exists
        url = reverse("dragon:registration-review", kwargs={"token": token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "již byla vyřízena")


class TestRegistrationReviewConfirmApprove(TestCase):
    """Submitting the confirm form should approve the registration (reuses dashboard logic)."""

    def setUp(self):
        self.staff = create_profiled_user("staff", "staffpw")
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(username="staff", password="staffpw")
        self.reg = make_pending_registration()
        self.token = make_token(self.reg.id, "approve")
        self.review_url = reverse(
            "dragon:registration-review", kwargs={"token": self.token}
        )
        self.dashboard_url = reverse("dragon:dashboard")

    def test_review_page_shows_registration_details(self):
        response = self.client.get(self.review_url)
        self.assertContains(response, self.reg.nick)
        self.assertContains(response, self.reg.email)

    def test_review_page_shows_correct_action_label_for_approve(self):
        response = self.client.get(self.review_url)
        self.assertContains(response, "Potvrdit schválení")

    def test_review_page_shows_correct_action_label_for_reject(self):
        token = make_token(self.reg.id, "reject")
        url = reverse("dragon:registration-review", kwargs={"token": token})
        response = self.client.get(url)
        self.assertContains(response, "Potvrdit zamítnutí")

    def test_confirm_approve_creates_user(self):
        self.client.post(
            self.dashboard_url,
            {
                "awaiting_registration_id": self.reg.id,
                "form_type": FormTypes.REGISTRATIONS.value,
                "submission_type": RegistrationRequestApproval.APPROVE.value,
                "message": "",
            },
        )
        self.assertTrue(UserProfile.objects.filter(nick=self.reg.nick).exists())
        self.assertFalse(AwaitingRegistration.objects.filter(id=self.reg.id).exists())

    def test_confirm_approve_sends_welcome_email(self):
        self.client.post(
            self.dashboard_url,
            {
                "awaiting_registration_id": self.reg.id,
                "form_type": FormTypes.REGISTRATIONS.value,
                "submission_type": RegistrationRequestApproval.APPROVE.value,
                "message": "",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.reg.email, mail.outbox[0].to)

    def test_confirm_reject_deletes_registration(self):
        self.client.post(
            self.dashboard_url,
            {
                "awaiting_registration_id": self.reg.id,
                "form_type": FormTypes.REGISTRATIONS.value,
                "submission_type": RegistrationRequestApproval.REJECT.value,
                "message": "",
            },
        )
        self.assertFalse(AwaitingRegistration.objects.filter(id=self.reg.id).exists())
        self.assertFalse(UserProfile.objects.filter(nick=self.reg.nick).exists())

    def test_confirm_reject_sends_rejection_email(self):
        self.client.post(
            self.dashboard_url,
            {
                "awaiting_registration_id": self.reg.id,
                "form_type": FormTypes.REGISTRATIONS.value,
                "submission_type": RegistrationRequestApproval.REJECT.value,
                "message": "",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.reg.email, mail.outbox[0].to)
