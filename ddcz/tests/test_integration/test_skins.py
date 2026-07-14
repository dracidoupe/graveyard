from django.test import Client, TestCase

from django.urls import reverse

from ..model_generator import create_profiled_user


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

    def test_skin_links_preserve_current_page_query_parameters(self):
        self.client.force_login(create_profiled_user("test-user", "password"))
        res = self.client.get(reverse("ddcz:news"), {"z_s": 3, "order": "author"})

        self.assertContains(res, "redirect=/aktuality/%3Fz_s%3D3%26order%3Dauthor")
