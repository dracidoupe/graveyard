from django.test import Client, TestCase

from django.urls import reverse


class SkinRedirectTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_redirect_to_same_page(self):
        res = self.client.get(
            reverse("ddcz:change-skin"), {"skin": "dark", "redirect": "/forum/"}
        )

        self.assertEquals("/forum/", res.url)

    def test_redirect_out_of_site_redirects_to_root(self):
        res = self.client.get(
            reverse("ddcz:change-skin"),
            {"skin": "dark", "redirect": "https://google.com"},
        )

        self.assertEquals("/", res.url)
