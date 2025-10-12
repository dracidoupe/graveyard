from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ddcz.models import UserProfile
from ddcz.tests.model_generator import create_profiled_user


class TestDragonUserBan(TestCase):
    def setUp(self):
        # Create staff user and log in
        self.staff = User.objects.create_user(username="staff", password="staffpw")
        self.staff.is_staff = True
        self.staff.save()
        # Staff user needs profile for middleware
        staff_profile = UserProfile(
            nick="staff", email="staff@example.com", user=self.staff
        )
        staff_profile.save()
        self.client.login(username="staff", password="staffpw")

        # Create a normal user to ban/unban
        self.user = create_profiled_user("victim", "secret")
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.status = "4"
        self.profile.save()

        self.ban_url = reverse("dragon:user-ban", kwargs={"user_id": self.user.id})
        self.unban_url = reverse("dragon:user-unban", kwargs={"user_id": self.user.id})

    def test_ban_user(self):
        response = self.client.post(self.ban_url, follow=True)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.status, "1")
        self.assertContains(response, "zablokován")

    def test_unban_user(self):
        # First ban
        self.client.post(self.ban_url)
        # Then unban
        response = self.client.post(self.unban_url, follow=True)
        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.status, "1")
        self.assertEqual(self.profile.status, "4")
        self.assertContains(response, "odblokován")

    def test_requires_staff(self):
        # Log out staff
        self.client.logout()
        # Create non-staff user
        User.objects.create_user(username="norm", password="pw")
        self.client.login(username="norm", password="pw")

        self.client.post(self.ban_url, follow=True)
        # staff_member_required redirects to login; ensure status unchanged
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.status, "4")
