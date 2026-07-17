from django.test import SimpleTestCase

from ddcz.models import UserProfile


class TestSlugGenerator(SimpleTestCase):
    def test_simple(self):
        a = UserProfile(nick="ahoj a hola")
        self.assertEqual("ahoj-a-hola", a.slug)

    def test_upper(self):
        a = UserProfile(nick="ahoj a HOLA")
        self.assertEqual("ahoj-a-hola", a.slug)

    def test_combining(self):
        a = UserProfile(nick="ahoj a ďíky")
        self.assertEqual("ahoj-a-diky", a.slug)

    def test_strip_noncombining(self):
        a = UserProfile(nick="ahoj a 你好")
        self.assertEqual("ahoj-a", a.slug)
