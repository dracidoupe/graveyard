from selenium.webdriver.common.by import By

from ..cases import SeleniumTestCase, MainPage
from ...attack_strings import IMG_TAB_SRC_INPUT
from ...model_generator import get_alphabetic_user_profiles, get_tavern_tables
from .pages_tavern import TavernTableListPage, TavernTablePostPage


class TestTavernPosts(SeleniumTestCase):
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

    def navigate_to_bookmarked_table(self, user_profile, table):
        self.navigate_to_tavern(user_profile)
        self.selenium.find_element(
            By.XPATH,
            TavernTableListPage.TAVERN_TABLE_LINK_TEMPLATE.value.format(
                table_id=table.id
            ),
        ).click()

    def select_listing(self, listing):
        self.selenium.find_element(
            By.XPATH,
            TavernTableListPage.NAVIGATION_LIST_STYLE_TEMPLATE.value.format(
                slug=listing
            ),
        ).click()

    def add_post(self, text):
        self.el(TavernTablePostPage.POST_TEXTAREA).send_keys(text)
        self.el(TavernTablePostPage.POST_SUBMIT).click()

    def test_owner_can_post(self):
        self.navigate_to_bookmarked_table(
            self.owner, self.tables["bookmarked_public_table"]
        )
        self.add_post(IMG_TAB_SRC_INPUT)

        text = self.selenium.find_element(
            By.XPATH, TavernTablePostPage.FIRST_COMMENT.value
        ).text

        self.assertEquals(IMG_TAB_SRC_INPUT, text)
