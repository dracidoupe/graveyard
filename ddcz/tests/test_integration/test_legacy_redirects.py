from unittest import TestCase

from django.template import Context, Template
from django.test import Client

from ddcz.models import Quest


class TestDobrodruztviRedirect(TestCase):
    def setUp(self):
        self.quest = Quest.objects.create(
            id=21,
            name="Test quest",
            abstract="yolo",
            keywords="test, quest",
        )
        self.client = Client()

    def test_dobrodruzstvi_without_suffix(self):
        response = self.client.get(f"/dobrodruzstvi/{self.quest.id}/")
        self.assertEquals(response.status_code, 301)
        self.assertEquals(
            response.url, f"/dobrodruzstvi/{self.quest.id}-{self.quest.get_slug()}/"
        )
