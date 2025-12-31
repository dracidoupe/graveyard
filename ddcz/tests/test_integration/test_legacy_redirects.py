from django.test import Client, TestCase

from ddcz.models import (
    ApprovalChoices,
    CommonArticle,
    RangerSpell,
    Skill,
    UserProfile,
    Quest,
)
from ddcz.tests.model_generator import get_valid_article_chain


class RedirectTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.create_creation()
        self.client = Client()

    def assert_redirect(self, from_url, to_url_prefix):
        response = self.client.get(from_url)
        self.assertEquals(response.status_code, 301)
        self.assertEquals(
            response.url,
            f"{to_url_prefix}/{self.creation.id}-{self.creation.get_slug()}/",
        )


class TestQuestRedirect(RedirectTestCase):
    def create_creation(self):
        self.creation = Quest.objects.create(
            id=21,
            name="Test quest",
            abstract="yolo",
            keywords="test, quest",
        )

    def test_redirect(self):
        self.assert_redirect(f"/dobrodruzstvi/{self.creation.id}/", "/dobrodruzstvi")


class TestSkillPrintRedirect(RedirectTestCase):
    def create_creation(self):
        self.creation = Skill.objects.create(
            id=1, name="Test skill", description="yolo"
        )

    def test_redirect(self):
        self.assert_redirect(
            f"/code/dovednosti/dovednosti_tisk.php?id={self.creation.id}",
            "/rubriky/dovednosti",
        )


class TestRangerSpellRedirect(RedirectTestCase):
    def create_creation(self):
        self.creation = RangerSpell.objects.create(
            name="Super Kouzlo",
            magenergy=1,
            is_published=ApprovalChoices.APPROVED.value,
        )

    def test_redirect(self):
        self.assert_redirect(
            f"/code/hranicarkouzla/hranicarkouzla_tisk.php?id={self.creation.id}",
            "/rubriky/hranicarkouzla",
        )


class TestUserProfileRedirect(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserProfile.objects.create(id=1, nick="test")
        self.client = Client()

    def test_redirect(self):
        response = self.client.get(
            f"/index.php?rub=uzivatele_podrobnosti&skin=light&id={self.user.id}"
        )
        self.assertEquals(response.status_code, 301)
        self.assertEquals(response.url, f"/uzivatel/{self.user.id}-test/")


class TestCommonArticlePrintRedirect(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

        # Create base objects for articles
        noverasy_chain = get_valid_article_chain()
        noverasy_chain["user"].save()
        noverasy_chain["author"].save()

        hranicar_chain = get_valid_article_chain()
        hranicar_chain["user"].nick = "Author2"
        hranicar_chain["user"].email = "test2@example.com"
        hranicar_chain["user"].save()
        hranicar_chain["author"].id = 2
        hranicar_chain["author"].save()

        clanky_chain = get_valid_article_chain()
        clanky_chain["user"].nick = "Author3"
        clanky_chain["user"].email = "test3@example.com"
        clanky_chain["user"].save()
        clanky_chain["author"].id = 3
        clanky_chain["author"].save()

        # Create test articles for each category we want to test
        self.noverasy_article = CommonArticle.objects.create(
            id=774,
            name="Test nové rasy",
            author=noverasy_chain["author"],
            author_nick=noverasy_chain["user"].nick,
            author_mail=noverasy_chain["user"].email,
            is_published=CommonArticle.CREATION_APPROVED,
            creative_page_slug="noverasy",
            section="noverasy",
        )

        self.hranicar_article = CommonArticle.objects.create(
            id=408,
            name="Test hraničář",
            author=hranicar_chain["author"],
            author_nick=hranicar_chain["user"].nick,
            author_mail=hranicar_chain["user"].email,
            is_published=CommonArticle.CREATION_APPROVED,
            creative_page_slug="hranicar",
            section="hranicar",
        )

        self.clanky_article = CommonArticle.objects.create(
            id=2682,
            name="Test článek",
            author=clanky_chain["author"],
            author_nick=clanky_chain["user"].nick,
            author_mail=clanky_chain["user"].email,
            is_published=CommonArticle.CREATION_APPROVED,
            creative_page_slug="clanky",
            section="clanky",
        )

    def test_noverasy_print_redirect(self):
        """Test the redirect for noverasy print URLs"""
        url = "/code/prispevky/prispevky_tisk.php"
        response = self.client.get(f"{url}?id=774&co=noverasy&skin=dark")

        # Now we expect the correct behavior
        self.assertEquals(response.status_code, 301)
        self.assertEquals(
            response.url,
            f"/rubriky/noverasy/{self.noverasy_article.id}-{self.noverasy_article.get_slug()}/",
        )

    def test_hranicar_print_redirect(self):
        """Test the redirect for hranicar print URLs"""
        url = "/code/prispevky/prispevky_tisk.php"
        response = self.client.get(f"{url}?id=408&co=hranicar&skin=dark")

        # Now we expect the correct behavior
        self.assertEquals(response.status_code, 301)
        self.assertEquals(
            response.url,
            f"/rubriky/hranicar/{self.hranicar_article.id}-{self.hranicar_article.get_slug()}/",
        )

    def test_clanky_print_redirect(self):
        """Test the redirect for clanky print URLs"""
        url = "/code/prispevky/prispevky_tisk.php"
        response = self.client.get(f"{url}?id=2682&co=clanky&skin=dark")

        # Now we expect the correct behavior
        self.assertEquals(response.status_code, 301)
        self.assertEquals(
            response.url,
            f"/rubriky/clanky/{self.clanky_article.id}-{self.clanky_article.get_slug()}/",
        )


class TestLegacyRedirectErrors(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_print_legacy_router_invalid_id(self):
        # This matches the error from Sentry: /code/alchpredmety/alchpredmety_tisk.php?id=535'
        url = "/code/alchpredmety/alchpredmety_tisk.php"
        response = self.client.get(f"{url}?id=535'")
        self.assertEqual(response.status_code, 400)

    def test_legacy_router_invalid_id(self):
        # Also testing the main legacy_router (index.php)
        url = "/index.php"
        response = self.client.get(f"{url}?rub=alchpredmety_jeden&id=535'")
        self.assertEqual(response.status_code, 400)
