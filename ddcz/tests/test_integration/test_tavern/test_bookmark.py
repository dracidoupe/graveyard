from django.test import Client, TestCase
from django.urls import reverse

from ddcz.models import TavernBookmark
from ddcz.tavern import bookmark_table, create_tavern_table

from ...model_generator import get_alphabetic_user_profiles


class TestTableBookmark(TestCase):
    def setUp(self):
        self.profile = get_alphabetic_user_profiles(
            number_of_users=1, saved=True, with_corresponding_user=True
        )[0]
        self.table = create_tavern_table(
            owner=self.profile,
            public=True,
            name="Public",
            description="Public Tavern Table",
        )
        self.bookmark_url = reverse("ddcz:tavern-bookmark", args=[self.table.pk])
        self.posts_url = reverse("ddcz:tavern-posts", args=[self.table.pk])
        self.client = Client()
        self.client.force_login(self.profile.user)

    def test_get_does_not_change_bookmark_state(self):
        response = self.client.get(self.bookmark_url, {"action": "oblibit"})

        self.assertEqual(405, response.status_code)
        self.assertFalse(
            TavernBookmark.objects.filter(
                tavern_table=self.table, user_profile=self.profile
            ).exists()
        )

    def test_post_books_table(self):
        response = self.client.post(self.bookmark_url, {"action": "oblibit"})

        self.assertRedirects(response, self.posts_url)
        self.assertTrue(
            TavernBookmark.objects.filter(
                tavern_table=self.table, user_profile=self.profile
            ).exists()
        )

    def test_post_unbooks_table(self):
        bookmark_table(self.profile, self.table)

        response = self.client.post(self.bookmark_url, {"action": "neoblibit"})

        self.assertRedirects(response, self.posts_url)
        self.assertFalse(
            TavernBookmark.objects.filter(
                tavern_table=self.table, user_profile=self.profile
            ).exists()
        )

    def test_post_rejects_invalid_action(self):
        response = self.client.post(self.bookmark_url, {"action": "invalid"})

        self.assertEqual(400, response.status_code)

    def test_post_rejects_missing_action(self):
        response = self.client.post(self.bookmark_url)

        self.assertEqual(400, response.status_code)

    def test_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.profile.user)

        response = csrf_client.post(self.bookmark_url, {"action": "oblibit"})

        self.assertEqual(403, response.status_code)
        self.assertFalse(
            TavernBookmark.objects.filter(
                tavern_table=self.table, user_profile=self.profile
            ).exists()
        )

    def test_table_page_renders_bookmark_form(self):
        response = self.client.get(self.posts_url)

        self.assertContains(
            response, f'<form method="post" action="{self.bookmark_url}">'
        )
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'name="action" value="oblibit"')
