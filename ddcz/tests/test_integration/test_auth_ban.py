from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ddcz.models import UserProfile
from ddcz.tests.model_generator import create_profiled_user


class TestAuthBanning(TestCase):
    def setUp(self):
        self.login_url = reverse("ddcz:login-action")
        self.news_url = reverse("ddcz:news")

    def test_banned_user_cannot_login(self):
        # Arrange: create user and ban them
        user = create_profiled_user("banned", "secret")
        profile = UserProfile.objects.get(pk=user.id)
        profile.status = "1"  # legacy: 1 = banned
        profile.save()

        # Act: try to log in
        response = self.client.post(
            self.login_url,
            {"nick": "banned", "password": "secret"},
            follow=True,
            HTTP_REFERER=self.news_url,
        )

        # Assert: not authenticated and message shown
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = (
            list(response.context["messages"]) if "messages" in response.context else []
        )
        self.assertTrue(any("zablokován" in str(m) for m in messages))

    def test_unbanned_user_can_login(self):
        # Arrange: create user and ensure unbanned status
        user = create_profiled_user("okuser", "secret")
        profile = UserProfile.objects.get(pk=user.id)
        profile.status = "4"  # normal working user
        profile.save()

        # Act: login
        response = self.client.post(
            self.login_url,
            {"nick": "okuser", "password": "secret"},
            follow=True,
            HTTP_REFERER=self.news_url,
        )

        # Assert: authenticated and no ban message
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        messages = (
            list(response.context["messages"]) if "messages" in response.context else []
        )
        self.assertFalse(any("zablokován" in str(m) for m in messages))

    def test_login_updates_last_login(self):
        user = create_profiled_user("testuser", "secret")
        profile = UserProfile.objects.get(pk=user.id)
        profile.status = "4"
        old_last_login = timezone.now() - timedelta(days=1)
        profile.last_login = old_last_login
        profile.save()

        self.client.post(
            self.login_url,
            {"nick": "testuser", "password": "secret"},
            follow=True,
            HTTP_REFERER=self.news_url,
        )
        profile.refresh_from_db()
        self.assertGreater(profile.last_login, old_last_login)
