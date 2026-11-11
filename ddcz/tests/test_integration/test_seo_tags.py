import json
import re

from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase

from ddcz.creations import ApprovalChoices
from ddcz.models import CommonArticle, GalleryPicture, Monster


class SeoTagsTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        cache.clear()
        self.client = Client()
        base = settings.EMAIL_LINKS_BASE_URI.rstrip("/")
        self.base = base

        self.article = CommonArticle.objects.create(
            pk=1,
            name="xoxo",
            author_nick="Autor",
            creative_page_slug="clanky",
            is_published=ApprovalChoices.APPROVED.value,
            abstract="Anotace k eseji o kyklopech",
            text="&lt;p&gt;Dlouhý text eseje.&lt;/p&gt;",
        )

    def get_json_ld(self, res):
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            res.content.decode(),
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))

    def test_article_detail_head(self):
        res = self.client.get("/rubriky/clanky/1-xoxo/?z_s=2&l=50")

        self.assertContains(
            res, "<title>xoxo – Články&amp;Eseje | DraciDoupe.cz</title>", html=False
        )
        self.assertContains(
            res, '<meta name="description" content="Anotace k eseji o kyklopech">'
        )
        self.assertContains(
            res,
            f'<link rel="canonical" href="{self.base}/rubriky/clanky/1-xoxo/">',
        )
        self.assertContains(res, '<meta property="og:type" content="article">')
        self.assertContains(
            res,
            f'<meta property="og:url" content="{self.base}/rubriky/clanky/1-xoxo/">',
        )
        self.assertContains(
            res,
            '<meta property="og:description" content="Anotace k eseji o kyklopech">',
        )
        self.assertRegex(
            res.content.decode(),
            r'<meta property="og:image" content="http://[^"]+logo\.gif">',
        )

    def test_article_synopsis_rendered(self):
        res = self.client.get("/rubriky/clanky/1-xoxo/")
        self.assertContains(res, '<p class="synopsis">Anotace k eseji o kyklopech</p>')

    def test_article_json_ld(self):
        res = self.client.get("/rubriky/clanky/1-xoxo/")
        data = self.get_json_ld(res)

        self.assertEqual("Article", data["@type"])
        self.assertEqual("xoxo", data["headline"])
        self.assertEqual("Autor", data["author"]["name"])
        self.assertEqual(f"{self.base}/rubriky/clanky/1-xoxo/", data["url"])

    def test_single_h1_with_creation_name(self):
        res = self.client.get("/rubriky/clanky/1-xoxo/")
        content = res.content.decode()

        self.assertEqual(1, content.count("<h1"))
        self.assertRegex(content, r'<h1 class="creation-heading">xoxo')
        self.assertContains(res, '<a href="/rubriky/clanky/">Články&amp;Eseje</a>')

    def test_monster_description_from_stats(self):
        Monster.objects.create(
            pk=1,
            name="Kyklop",
            author_nick="Autor",
            is_published=ApprovalChoices.APPROVED.value,
            group="Ostatní",
            size="D",
            hitpoint_class="10",
            attack="7",
            description="&lt;p&gt;Obr s jedním okem.&lt;/p&gt;",
            rating=0,
        )

        res = self.client.get("/rubriky/bestiar/1-kyklop/")

        self.assertContains(res, "<title>Kyklop – Bestiář | DraciDoupe.cz</title>")
        self.assertContains(
            res,
            'content="Ostatní, velikost D, ŽT 10, ÚČ 7. Obr s jedním okem."',
        )

    def test_gallery_picture_uses_own_image_for_og(self):
        GalleryPicture.objects.create(
            pk=1,
            name="Drak",
            author_nick="Autor",
            is_published=ApprovalChoices.APPROVED.value,
            image_path="drak.jpg",
            image_thumbnail_path="drak-small.jpg",
            rating=0,
        )

        res = self.client.get("/rubriky/galerie/1-drak/")

        self.assertContains(
            res,
            '<meta property="og:image" content="https://uploady.dracidoupe.cz/galerie/drak.jpg">',
        )

    def test_list_first_page(self):
        res = self.client.get("/rubriky/clanky/")

        self.assertContains(
            res, "<title>Články&amp;Eseje | DraciDoupe.cz</title>", html=False
        )
        self.assertContains(res, '<meta name="description" content="Články')
        self.assertContains(
            res, f'<link rel="canonical" href="{self.base}/rubriky/clanky/">'
        )
        self.assertEqual(1, res.content.decode().count("<h1"))

    def test_list_later_page_is_self_canonical(self):
        CommonArticle.objects.bulk_create(
            [
                CommonArticle(
                    pk=100 + i,
                    name=f"clanek {i}",
                    creative_page_slug="clanky",
                    is_published=ApprovalChoices.APPROVED.value,
                )
                for i in range(30)
            ]
        )

        res = self.client.get("/rubriky/clanky/?z_s=2")

        self.assertContains(
            res, "<title>Články&amp;Eseje, strana 2 | DraciDoupe.cz</title>", html=False
        )
        self.assertContains(
            res,
            f'<link rel="canonical" href="{self.base}/rubriky/clanky/?z_s=2">',
        )

    def test_news_page(self):
        res = self.client.get("/aktuality/")

        self.assertContains(res, "<title>Aktuality | DraciDoupe.cz</title>")
        self.assertContains(res, "nestvůr do bestiáře")
        self.assertEqual(1, res.content.decode().count("<h1"))
