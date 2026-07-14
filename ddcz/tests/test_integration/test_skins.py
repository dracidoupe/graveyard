import struct

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
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

    def test_page_uses_correct_favicon_formats_for_each_skin(self):
        for skin in ("light", "dark", "historic"):
            with self.subTest(skin=skin):
                session = self.client.session
                session["skin"] = skin
                session.save()

                response = self.client.get("/aktuality/")

                self.assertContains(
                    response,
                    f'<link rel="icon" type="image/x-icon" href="{staticfiles_storage.url(f"skins/{skin}/img/drak.ico")}">',
                    html=True,
                )
                self.assertContains(
                    response,
                    f'<link rel="icon" type="image/svg+xml" href="{staticfiles_storage.url(f"skins/{skin}/img/drak.svg")}">',
                    html=True,
                )
                self.assertContains(
                    response,
                    f'<link rel="apple-touch-icon" href="{staticfiles_storage.url(f"skins/{skin}/img/drak.png")}">',
                    html=True,
                )

    def test_apple_touch_icon_urls_redirect_to_current_skin_png(self):
        session = self.client.session
        session["skin"] = "dark"
        session.save()
        expected_url = staticfiles_storage.url("skins/dark/img/drak.png")

        for url in ("/apple-touch-icon.png", "/apple-touch-icon-precomposed.png"):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertRedirects(
                    response,
                    expected_url,
                    fetch_redirect_response=False,
                )

    def test_apple_touch_icons_are_180_pixel_pngs(self):
        for skin in ("light", "dark", "historic"):
            with self.subTest(skin=skin):
                icon_path = finders.find(f"skins/{skin}/img/drak.png")

                self.assertIsNotNone(icon_path)
                with open(icon_path, "rb") as icon_file:
                    png_header = icon_file.read(24)

                self.assertEqual(png_header[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", png_header[16:24]), (180, 180))
