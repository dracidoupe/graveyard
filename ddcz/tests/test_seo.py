import json
from datetime import UTC, datetime

from django.test import SimpleTestCase, TestCase

from ddcz.models import CommonArticle, CreativePage, Monster
from ddcz.seo import (
    DESCRIPTION_MAX_LENGTH,
    creation_description,
    creation_json_ld,
    meta_description,
    plain_text,
)


class PlainTextTestCase(SimpleTestCase):
    def test_strips_entity_encoded_tags(self):
        self.assertEqual(
            "Silný kyklop žije v jeskyni.",
            plain_text(
                "&lt;p&gt;Silný &lt;b&gt;kyklop&lt;/b&gt; žije v jeskyni.&lt;/p&gt;"
            ),
        )

    def test_double_encoded_nbsp_becomes_space(self):
        self.assertEqual("a b", plain_text("a&amp;nbsp;b"))

    def test_collapses_whitespace(self):
        self.assertEqual("a b c", plain_text("a\n\n  b\t c "))

    def test_empty_values(self):
        self.assertEqual("", plain_text(None))
        self.assertEqual("", plain_text(""))


class MetaDescriptionTestCase(SimpleTestCase):
    def test_truncated_to_limit(self):
        description = meta_description("slovo " * 100)
        self.assertLessEqual(len(description), DESCRIPTION_MAX_LENGTH)
        self.assertTrue(description.endswith("…"))

    def test_short_text_untouched(self):
        self.assertEqual("Krátký text", meta_description("Krátký text"))


class CreationDescriptionTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        self.page = CreativePage.objects.get(slug="clanky")

    def test_article_prefers_abstract(self):
        article = CommonArticle(
            name="Esej",
            abstract="Krátká anotace",
            text="&lt;p&gt;Dlouhý text&lt;/p&gt;",
        )
        self.assertEqual("Krátká anotace", creation_description(article, self.page))

    def test_article_falls_back_to_text(self):
        article = CommonArticle(
            name="Esej", abstract="", text="&lt;p&gt;Dlouhý text&lt;/p&gt;"
        )
        self.assertEqual("Dlouhý text", creation_description(article, self.page))

    def test_empty_creation_falls_back_to_name(self):
        article = CommonArticle(name="Esej", abstract="", text="")
        self.assertEqual(
            f"Esej – {self.page.name} na DraciDoupe.cz",
            creation_description(article, self.page),
        )

    def test_monster_gets_stat_prefix(self):
        monster = Monster(
            name="Kyklop",
            group="Ostatní",
            size="D",
            hitpoint_class="10",
            attack="7",
            description="&lt;p&gt;Obr s jedním okem.&lt;/p&gt;",
        )
        self.assertEqual(
            "Ostatní, velikost D, ŽT 10, ÚČ 7. Obr s jedním okem.",
            creation_description(monster, self.page),
        )


class CreationJsonLdTestCase(SimpleTestCase):
    def test_script_breaking_content_is_escaped(self):
        article = CommonArticle(
            name="</script><script>alert(1)</script>",
            author_nick="Autor",
            published=datetime(2020, 1, 2, 3, 4, 5, tzinfo=UTC),
        )
        page = CreativePage(name="Články", slug="clanky")

        output = creation_json_ld(
            article, page, "https://www.dracidoupe.cz/x/", "Popis & více"
        )

        self.assertNotIn("</script>", output)
        data = json.loads(output)
        self.assertEqual("Article", data["@type"])
        self.assertEqual("Autor", data["author"]["name"])
        self.assertEqual("2020-01-02T03:04:05+00:00", data["datePublished"])
        self.assertEqual("Popis & více", data["description"])
        self.assertNotIn("image", data)
