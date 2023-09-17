from urllib.request import urlopen
from django.conf import settings

from selenium.webdriver.common.by import By

from .cases import SeleniumTestCase


class TestNews(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.selenium.get("%s%s" % (self.live_server_url, "/aktuality/"))

    def test_server_available(self):
        req = urlopen(self.live_server_url)
        self.assertEquals(200, req.code)

    def test_window_title_present(self):
        self.assertEquals("DraciDoupe.cz", self.selenium.title)

    def test_page_heading_present(self):
        text = self.selenium.find_element(
            By.XPATH, '//h1[contains(@class,"page-heading")]'
        ).text
        self.assertEquals("Aktuality", text)
