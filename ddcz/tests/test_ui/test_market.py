from enum import Enum

from selenium.webdriver.common.by import By

from ..model_generator import create_market_entries
from .cases import MainPage, SeleniumTestCase


class MarketPage(Enum):
    FIRST_SECTION_LINK = '//div[@id=page-market"]//article[@class="market]//a'
    # POST_TEXTAREA = '//textarea[@id="id_text"]'
    # POST_SUBMIT = '//*[@value="Přidej"]'


class TestMarket(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        self.entries = create_market_entries()
        self.first_entry = self.entries[0]

        self.selenium.get("{}{}".format(self.live_server_url, "/"))
        self.navigate_to_market()

    def navigate_to_market(self):
        self.el(MainPage.NAVIGATION_MARKET).click()
        self.assertEqual(
            "Inzerce",
            self.el(MainPage.MAIN_TITLE).text,
        )

    def test_page_heading_present(self):
        text = self.selenium.find_element(By.XPATH, '//h1[@class="page-heading"]').text
        self.assertEqual("Inzerce", text)

    def test_entry_text_rendered(self):
        text = self.selenium.find_element(
            By.XPATH, '//div[@id="page-market"]//span[contains(@class, "market_text")]'
        ).text
        self.assertEqual("Seller Text #0", text)
