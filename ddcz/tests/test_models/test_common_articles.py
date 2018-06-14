from unittest import TestCase

from ddcz.models import CommonArticle

class TestSlugGenerator(TestCase):
    def test_simple(self):
        a = CommonArticle(jmeno='ahoj a hola')
        self.assertEquals('ahoj-a-hola', a.get_slug())

    def test_upper(self):
        a = CommonArticle(jmeno='ahoj a HOLA')
        self.assertEquals('ahoj-a-hola', a.get_slug())

    def test_combining(self):
        a = CommonArticle(jmeno='ahoj a ďíky')
        self.assertEquals('ahoj-a-diky', a.get_slug())

    def test_strip_noncombining(self):
        a = CommonArticle(jmeno='ahoj a 你好')
        self.assertEquals('ahoj-a', a.get_slug())
