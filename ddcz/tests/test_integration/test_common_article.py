from django.test import Client, TestCase

from ddcz.models import CommonArticle


class ArticleAccessTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

        self.article = CommonArticle(pk=1, name="xoxo")
        self.article.save()

    def test_article_present(self):
        res = self.client.get("/rubriky/clanky/1-xoxo/")
        self.assertEquals(200, res.status_code)

    def test_bad_slug_redirect(self):
        res = self.client.get("/rubriky/clanky/1-bad-slug/")
        self.assertEquals(301, res.status_code)

        res = self.client.get("/rubriky/clanky/1-bad-slug/", follow=True)
        self.assertEquals([("/rubriky/clanky/1-xoxo/", 301)], res.redirect_chain)
        self.assertEquals(200, res.status_code)

    def test_redirect_for_empty_slug(self):
        article = CommonArticle(pk=2, name=" ")
        article.save()

        res = self.client.get("/rubriky/clanky/2-random-slug/", follow=True)
        self.assertEquals([("/rubriky/clanky/2-dilo/", 301)], res.redirect_chain)
        self.assertEquals(200, res.status_code)
