from .cases import SeleniumTestCase
from selenium.webdriver.common.by import By

from ddcz.models import CreativePage


class TestCreativePageRendered(SeleniumTestCase):
    fixtures = ["pages"]

    def test_page_heading_present(self):
        pages = CreativePage.objects.all()

        self.assertGreater(len(pages), 5)

        for page in pages:
            self.selenium.get(
                "%s%s" % (self.live_server_url, "/rubriky/%s/" % page.slug)
            )

            text = self.selenium.find_element(
                By.XPATH, '//h1[contains(@class,"page-heading")]'
            ).text
            self.assertEquals("DraciDoupe.cz", self.selenium.title)
            self.assertEquals(page.name, text)
