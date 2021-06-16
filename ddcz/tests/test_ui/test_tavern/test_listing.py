from enum import Enum

from django.db import transaction

from ddcz.tavern import LIST_ALL
from ..cases import SeleniumTestCase
from ...model_generator import get_alphabetic_user_profiles, get_tavern_tables


class TavernTableListPage(Enum):
    URL = "/putyka/"
    TAVERN_TABLE_LIST_NAME = "//table[contains(@class, 'tavern-table-list')]//span[contains(@class, 'tavern-table-name')]"
    NAVIGATION_LIST_STYLE_TEMPLATE = "//a[@data-list-style='{slug}']"


class MainPage(Enum):
    BODY = "//body"
    MAIN_TITLE = "//h1[contains(@class, 'page-heading')]"
    LOGIN_USERNAME_INPUT = '//*[@id="id_nick"]'
    LOGIN_PASSWORD_INPUT = '//*[@id="id_password"]'
    LOGIN_SUBMIT = '//*[@id="login_submit"]'
    LOGOUT_SUBMIT = '//*[@id="logout_submit"]'
    CONTROL_NICK = '//*[@id="ddcz_nick"]'

    NAVIGATION_TAVERN = '//*[@id="ddcz_nav_tavern"]'


class TestTavernListing(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        (
            self.owner,
            self.allowed_user,
            self.banned_user,
            self.visiting_user,
        ) = get_alphabetic_user_profiles(
            number_of_users=4, saved=True, with_corresponding_user=True
        )

        self.tables = get_tavern_tables(
            self.owner,
            self.allowed_user,
            self.banned_user,
            self.visiting_user,
        )

        self.selenium.get(self.live_server_url)

    def el(self, enum):
        return self.selenium.find_element_by_xpath(enum.value)

    def els(self, enum):
        return self.selenium.find_elements_by_xpath(enum.value)

    def is_logged_in(self):
        return self.el(MainPage.BODY).get_attribute("data-logged-in") == "1"

    def navigate_as_user(self, user_profile):
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
        self.el(MainPage.NAVIGATION_TAVERN).click()
        self.assertEquals(
            "Putyka",
            self.el(MainPage.MAIN_TITLE).text,
        )

    def select_listing(self, listing):
        self.selenium.find_element_by_xpath(
            TavernTableListPage.NAVIGATION_LIST_STYLE_TEMPLATE.value.format(
                slug=listing
            )
        ).click()

    def assertTablesInListing(self, expected_tables):
        rendered_table_names = [
            el.text for el in self.els(TavernTableListPage.TAVERN_TABLE_LIST_NAME)
        ]

        for table in expected_tables:
            self.assertIn(table.name, rendered_table_names)

    def test_owner_sees_bookmarks(self):
        self.navigate_as_user(self.owner)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
                self.tables["bookmarked_private_table"],
            ]
        )

    def test_owner_sees_everything(self):
        self.navigate_as_user(self.owner)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(self.tables.values())

    def test_allowed_user_sees_bookmarks(self):
        self.navigate_as_user(self.allowed_user)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
                self.tables["bookmarked_private_table"],
            ]
        )

    def test_allowed_user_sees_everything(self):
        self.navigate_as_user(self.allowed_user)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(self.tables.values())

    def test_visiting_user_sees_public(self):
        self.navigate_as_user(self.visiting_user)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
                self.tables["unbookmarked_public_table"],
            ]
        )

    def test_visiting_user_sees_public_bookmarked(self):
        self.navigate_as_user(self.visiting_user)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
            ]
        )
