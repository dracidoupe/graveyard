from django.test import SimpleTestCase

from ddcz.models import CommonArticle


class TestSlugGenerator(SimpleTestCase):
    def test_simple(self):
        a = CommonArticle(name="ahoj a hola")
        self.assertEquals("ahoj-a-hola", a.get_slug())

    def test_upper(self):
        a = CommonArticle(name="ahoj a HOLA")
        self.assertEquals("ahoj-a-hola", a.get_slug())

    def test_combining(self):
        a = CommonArticle(name="ahoj a ďíky")
        self.assertEquals("ahoj-a-diky", a.get_slug())

    def test_strip_noncombining(self):
        a = CommonArticle(name="ahoj a 你好")
        self.assertEquals("ahoj-a", a.get_slug())
