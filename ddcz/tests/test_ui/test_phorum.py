from enum import Enum

from ddcz.models import Phorum

from ..attack_strings import SCRIPT_ALERT_INPUT
from ..model_generator import get_alphabetic_user_profiles
from .cases import SeleniumTestCase


class PhorumPage(Enum):
    POST_TEXTAREA = '//textarea[@id="id_text"]'
    POST_SUBMIT = '//*[@value="Přidej"]'


class TestPhorum(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        self.user_profile = get_alphabetic_user_profiles(
            saved=True, with_corresponding_user=True
        )[0]

        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        self.navigate_to_phorum()
        self.post_comment()

    def navigate_to_phorum(self):
        return self.navigate_as_authenticated_user(
            user_profile=self.user_profile,
            navigation_element=self.main_page_nav.NAVIGATION_PHORUM,
            expected_title="Fórum",
        )

    def post_comment(self):
        self.el(PhorumPage.POST_TEXTAREA).send_keys(SCRIPT_ALERT_INPUT)
        self.el(PhorumPage.POST_SUBMIT).click()

    def test_page_heading_present(self):
        text = self.selenium.find_element_by_xpath('//h1[@class="page-heading"]').text
        self.assertEquals("Fórum", text)

    def test_author_rendered(self):
        text = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//span[@class="nick"]'
        ).text.strip()
        self.assertEquals(self.user_profile.nick, text)

    def test_comment_text_rendered(self):
        text = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//p[@class="comment_text"]'
        ).text
        self.assertEquals(SCRIPT_ALERT_INPUT, text)

    def test_author_link_rendered(self):
        url = self.selenium.find_element_by_xpath(
            '//div[@id="page-phorum"]//span[@class="nick"]/a'
        ).get_attribute("href")
        self.assertIn(self.user_profile.slug, url)
        self.assertIn(str(self.user_profile.pk), url)
