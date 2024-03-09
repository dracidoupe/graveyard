from django.template import Context, Template
from django.test import Client, TestCase

from ddcz.models import ApprovalChoices, CommonArticle, RangerSpell, Skill, Quest


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
