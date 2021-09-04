from enum import Enum
from time import sleep

from selenium.webdriver.support.ui import Select

from .cases import SeleniumTestCase, MainPage


class SignUpPage(Enum):
    NICK = '//*[@id="nickname"]'
    NAME_GIVEN = '//*[@id="first_name"]'
    NAME_FAMILY = '//*[@id="last_name"]'
    SEX = '//*[@id="sex"]'
    AGE = '//*[@id="age"]'
    SALUTATION = '//*[@id="addressing"]'
    EMAIL = '//*[@id="email"]'
    GDPR = '//*[@id="gdpr"]'
    POST_SUBMIT = '//input[@name="submit"]'

    CHARACTER_PARAGRAPHS = '//p[@class="character"]'


class TestValidSignupSubmission(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.selenium.get("%s%s" % (self.live_server_url, "/registrace/"))

        self.fill_valid_data()

    def fill_valid_data(self):
        self.nick = "přílišžluťoučkýkůňúělďábelskéó"

        self.el(SignUpPage.NICK).send_keys(self.nick)
        self.el(SignUpPage.NAME_GIVEN).send_keys(self.nick)
        self.el(SignUpPage.NAME_FAMILY).send_keys(self.nick)
        self.el(SignUpPage.SALUTATION).send_keys(self.nick)
        self.el(SignUpPage.AGE).send_keys(50)
        self.el(SignUpPage.EMAIL).send_keys("test@example.com")

        Select(self.el(SignUpPage.SEX)).select_by_value("F")

        Select(self.el(SignUpPage.GDPR)).select_by_value("T")

    def test_submission(self):
        # TODO: `text` does not contain the nick, and `get_css_attribute("::before") doesn't work

        # page_character_name = self.els(SignUpPage.CHARACTER_PARAGRAPHS)[0].text[
        #     0 : len(self.nick)
        # ]
        # self.assertEquals(self.nick, page_character_name)

        # This should wait implicitly in the modern selenium, but if flaky, add explicit wait
        self.el(SignUpPage.POST_SUBMIT).click()

        sleep(0.1)

        self.assertEquals(
            f"Vítej ve Městě, {self.nick}!", self.el(MainPage.MAIN_TITLE).text
        )
