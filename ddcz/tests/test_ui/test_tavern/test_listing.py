from enum import Enum
from urllib.request import urlopen
from django.conf import settings

from ddcz.models import Phorum

from ...model_generator import get_alphabetic_user_profiles, get_tavern_tables
from ..cases import SeleniumTestCase


class TavernPage(Enum):
    URL = "/putyka/"


class MainPage(Enum):
    MAIN_TITLE = "//h1[contains(@class, 'page-heading')]"
    LOGIN_USERNAME_INPUT = '//*[@id="id_nick"]'
    LOGIN_PASSWORD_INPUT = '//*[@id="id_password"]'
    LOGIN_SUBMIT = '//*[@id="login_submit"]'
    CONTROL_NICK = '//*[@id="ddcz_nick"]'

    NAVIGATION_TAVERN = '//*[@id="ddcz_nav_tavern"]'


class TestTavernListing(SeleniumTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        (
            cls.owner,
            cls.allowed_user,
            cls.banned_user,
            cls.visiting_user,
        ) = get_alphabetic_user_profiles(
            number_of_users=4, saved=True, with_corresponding_user=True
        )

        cls.tables = get_tavern_tables(
            cls.owner,
            cls.allowed_user,
            cls.banned_user,
            cls.visiting_user,
        )

        cls.selenium.get(cls.live_server_url)

    def el(self, enum):
        return self.__class__.selenium.find_element_by_xpath(enum.value)

    def navigate_as_user(self, user_profile):
        self.el(MainPage.LOGIN_USERNAME_INPUT).send_keys(user_profile.user.username)
        self.el(MainPage.LOGIN_PASSWORD_INPUT).send_keys(user_profile.user.email)
        self.el(MainPage.LOGIN_SUBMIT).submit()

        self.assertEquals(
            user_profile.nick,
            self.el(MainPage.CONTROL_NICK).text,
        )

        self.el(MainPage.NAVIGATION_TAVERN).click()

    def test_owner_sees_bookmarks(self):
        self.navigate_as_user(self.owner)

        self.assertEquals(
            "Putyka",
            self.el(MainPage.MAIN_TITLE).text,
        )
