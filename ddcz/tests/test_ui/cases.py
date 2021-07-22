from enum import Enum
import socket

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.decorators import classproperty

from selenium import webdriver


class MainPage(Enum):
    BODY = "//body"
    MAIN_TITLE = "//h1[contains(@class, 'page-heading')]"
    LOGIN_USERNAME_INPUT = '//*[@id="id_nick"]'
    LOGIN_PASSWORD_INPUT = '//*[@id="id_password"]'
    LOGIN_SUBMIT = '//*[@id="login_submit"]'
    LOGOUT_SUBMIT = '//*[@id="logout_submit"]'
    CONTROL_NICK = '//*[@id="ddcz_nick"]'

    NAVIGATION_TAVERN = '//*[@id="ddcz_nav_tavern"]'
    NAVIGATION_PHORUM = '//*[@id="ddcz_nav_phorum"]'


class SeleniumTestCase(StaticLiveServerTestCase):
    # We are always connect to all interfaces
    # to simplify the local and CI setup
    host = "0.0.0.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_page_nav = MainPage

    @classproperty
    def live_server_url(cls):
        return "http://%s:%s" % (
            getattr(settings, "TEST_LIVE_SERVER_HOST", None) or socket.gethostname(),
            cls.server_thread.port,
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if not settings.SELENIUM_HUB_HOST:
            cls.selenium = webdriver.Chrome()
        else:
            cls.selenium = webdriver.Remote(
                desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                command_executor="http://%s:4444/wd/hub" % settings.SELENIUM_HUB_HOST,
            )

        cls.selenium.implicitly_wait(settings.SELENIUM_IMPLICIT_WAIT)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    ###
    # Helper methods for navigating the specific DDCZ webpage
    ###

    def navigate_as_authenticated_user(
        self, user_profile, *, navigation_element, expected_title
    ):
        already_correct = False
        if self.is_logged_in():
            nick = self.el(MainPage.CONTROL_NICK).text
            if nick == user_profile.nick:
                already_correct = True
            else:
                self.el(MainPage.LOGOUT_SUBMIT).submit()

        if not already_correct:
            self.el(MainPage.LOGIN_USERNAME_INPUT).send_keys(user_profile.user.username)
            self.el(MainPage.LOGIN_PASSWORD_INPUT).send_keys(user_profile.user.email)
            self.el(MainPage.LOGIN_SUBMIT).submit()

        self.assertEquals(
            user_profile.nick,
            self.el(MainPage.CONTROL_NICK).text,
        )

        self.el(navigation_element).click()
        self.assertEquals(
            expected_title,
            self.el(MainPage.MAIN_TITLE).text,
        )

    ###
    # Helper methods to retrieve information from the current page
    ###

    def el(self, enum):
        return self.selenium.find_element_by_xpath(enum.value)

    def els(self, enum):
        return self.selenium.find_elements_by_xpath(enum.value)

    def is_logged_in(self):
        return self.el(MainPage.BODY).get_attribute("data-logged-in") == "1"
