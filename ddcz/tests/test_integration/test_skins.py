from django.test import Client, TestCase

from django.urls import reverse

from ddcz.tests.model_generator import create_profiled_user


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


class HistoricSkinLinksTestCase(TestCase):
    fixtures = ["pages"]

    def test_user_links_present(self):
        user = create_profiled_user("someone", "secret")
        self.client.login(username="someone", password="secret")
        session = self.client.session
        session["skin"] = "historic"
        session.save()

        res = self.client.get("/forum/")
        self.assertContains(res, reverse("ddcz:my-submissions"))
        self.assertContains(res, reverse("ddcz:user-settings"))
        self.assertNotContains(res, reverse("dragon:dashboard"))

        user.is_staff = True
        user.save()
        res = self.client.get("/forum/")
        self.assertContains(res, reverse("dragon:dashboard"))
