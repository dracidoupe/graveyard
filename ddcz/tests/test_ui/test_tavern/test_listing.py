from selenium.webdriver.common.by import By

from ddcz.tavern import LIST_ALL
from ..cases import SeleniumTestCase, MainPage
from ...model_generator import get_alphabetic_user_profiles, get_tavern_tables
from .pages_tavern import TavernTableListPage


class TestTavernListing(SeleniumTestCase):
    reset_sequences = True

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

    def navigate_to_tavern(self, user_profile):
        return self.navigate_as_authenticated_user(
            user_profile,
            navigation_element=MainPage.NAVIGATION_TAVERN,
            expected_title="Putyka",
        )

    def select_listing(self, listing):
        self.selenium.find_element(
            By.XPATH,
            TavernTableListPage.NAVIGATION_LIST_STYLE_TEMPLATE.value.format(
                slug=listing
            ),
        ).click()

    def assertTablesInListing(self, expected_tables):
        rendered_table_names = [
            el.text for el in self.els(TavernTableListPage.TAVERN_TABLE_LIST_NAME)
        ]

        for table in expected_tables:
            self.assertIn(table.name, rendered_table_names)

    def test_owner_sees_bookmarks(self):
        self.navigate_to_tavern(self.owner)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
                self.tables["bookmarked_private_table"],
            ]
        )

    def test_owner_sees_everything(self):
        self.navigate_to_tavern(self.owner)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(self.tables.values())

    def test_allowed_user_sees_bookmarks(self):
        self.navigate_to_tavern(self.allowed_user)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
                self.tables["bookmarked_private_table"],
            ]
        )

    def test_allowed_user_sees_everything(self):
        self.navigate_to_tavern(self.allowed_user)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(self.tables.values())

    # FIXME: Flaky test, but in CI only
    # unbookmarked is not there--so maybe switch from bookmark to all doesn't
    # happen fast enough?
    # def test_visiting_user_sees_public(self):
    #     self.navigate_as_user(self.visiting_user)
    #     self.select_listing(LIST_ALL)
    #
    #     self.assertTablesInListing(
    #         [
    #             self.tables["bookmarked_public_table"],
    #             self.tables["unbookmarked_public_table"],
    #         ]
    #     )

    def test_visiting_user_sees_public_bookmarked(self):
        self.navigate_to_tavern(self.visiting_user)
        self.select_listing(LIST_ALL)

        self.assertTablesInListing(
            [
                self.tables["bookmarked_public_table"],
            ]
        )
