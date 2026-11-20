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

        self.assertEqual("/forum/", res.url)

    def test_redirect_out_of_site_redirects_to_root(self):
        res = self.client.get(
            reverse("ddcz:change-skin"),
            {"skin": "dark", "redirect": "https://google.com"},
        )

        self.assertEqual("/", res.url)


class SkinMobileNavigationTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

    def get_news_page(self, skin):
        self.client.get(reverse("ddcz:change-skin"), {"skin": skin, "redirect": "/"})
        return self.client.get(reverse("ddcz:news")).content.decode("utf-8")

    def test_light_and_dark_have_jump_menu_and_its_targets(self):
        for skin in ["light", "dark"]:
            with self.subTest(skin=skin):
                page = self.get_news_page(skin)

                self.assertIn('id="jump_menu"', page)
                self.assertIn('id="to_top"', page)
                self.assertIn('id="left_menu"', page)
                self.assertIn('id="ostatni"', page)
                self.assertIn('id="ddcz_control"', page)

    def test_historic_has_no_jump_menu(self):
        page = self.get_news_page("historic")

        self.assertNotIn('id="jump_menu"', page)
        self.assertNotIn('id="to_top"', page)
