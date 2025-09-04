from enum import Enum
from time import sleep

from .cases import SeleniumTestCase, MainPage
from ddcz.models import AwaitingRegistration


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

    def fill_signup_form(self):
        self.nick = "přílišžluťoučkýkůňúělďábelskéó"

        self.el(SignUpPage.NICK).send_keys(self.nick)
        self.el(SignUpPage.NAME_GIVEN).send_keys(self.nick)
        self.el(SignUpPage.NAME_FAMILY).send_keys(self.nick)
        self.el(SignUpPage.SALUTATION).send_keys(self.nick)
        self.el(SignUpPage.AGE).send_keys(50)
        self.el(SignUpPage.EMAIL).send_keys("test@example.com")

        self.select_by_value(SignUpPage.SEX.value, "F")

        self.select_by_value(SignUpPage.GDPR.value, "T")

    def assert_registration_saved(self):
        self.assertEquals(
            1, AwaitingRegistration.objects.filter(nick=self.nick).count()
        )
        awaiting_registration = AwaitingRegistration.objects.get(nick=self.nick)
        self.assertEquals(self.nick, awaiting_registration.nick)
        self.assertEquals(self.nick, awaiting_registration.name_given)
        self.assertEquals(self.nick, awaiting_registration.name_family)
        self.assertEquals(self.nick, awaiting_registration.salutation)
        self.assertEquals(50, awaiting_registration.age)

    def test_submission(self):
        self.fill_signup_form()
        # wait for transition
        sleep(0.1)

        self.el(SignUpPage.POST_SUBMIT).click()
        # Wait for reload to start on computers that are too fast
        sleep(0.1)

        # Playwright auto-waits for navigation/render; directly assert the title
        self.assertEquals(
            f"Vítej ve Městě, {self.nick}!", self.el(MainPage.MAIN_TITLE).text
        )

        self.assert_registration_saved()
