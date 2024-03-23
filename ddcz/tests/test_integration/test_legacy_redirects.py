from django.test import Client, TestCase

from ddcz.models import (
    ApprovalChoices,
    RangerSpell,
    Skill,
    UserProfile,
    Quest,
)


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
