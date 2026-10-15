from django.test import Client, TestCase


class NotFoundPageTestCase(TestCase):
    fixtures = ["pages"]

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_custom_404_page_renders(self):
        response = self.client.get("/nekde-v-mlze/")

        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Dráček", status_code=404)
        self.assertContains(response, "Stránka se zatoulala", status_code=404)
        self.assertContains(response, "/nekde-v-mlze/", status_code=404)
        self.assertContains(
            response, "common/img/not-found-dragon.png", status_code=404
        )
        self.assertContains(response, 'href="/aktuality/"', status_code=404)
