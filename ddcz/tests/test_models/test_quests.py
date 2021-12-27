from django.test import SimpleTestCase

from ddcz.models import Quest


class TestQuestUrls(SimpleTestCase):
    def test_s3_url(self):
        a = Quest(pk=1, path="index.html", name="Name")
        self.assertEquals(
            "https://uploady.dracidoupe.cz/dobrodruzstvi/1/index.html",
            a.get_final_url(),
        )
