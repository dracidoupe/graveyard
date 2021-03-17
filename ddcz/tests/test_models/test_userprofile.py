from django.test import SimpleTestCase

from ddcz.models import UserProfile


class TestSlugGenerator(SimpleTestCase):
    def test_simple(self):
        a = UserProfile(nick_uzivatele="ahoj a hola")
        self.assertEquals("ahoj-a-hola", a.slug)

    def test_upper(self):
        a = UserProfile(nick_uzivatele="ahoj a HOLA")
        self.assertEquals("ahoj-a-hola", a.slug)

    def test_combining(self):
        a = UserProfile(nick_uzivatele="ahoj a ďíky")
        self.assertEquals("ahoj-a-diky", a.slug)

    def test_strip_noncombining(self):
        a = UserProfile(nick_uzivatele="ahoj a 你好")
        self.assertEquals("ahoj-a", a.slug)
