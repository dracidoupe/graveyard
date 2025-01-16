from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from .cases import SeleniumTestCase, MainPage
from ..model_generator import get_alphabetic_user_profiles
from .pages_dating import DatingListPage, DatingCreatePage
from ddcz.models import Dating
from ddcz.geo import CZECHOSLOVAK_REGIONS


class TestDating(SeleniumTestCase):
    reset_sequences = True

    def setUp(self):
        super().setUp()
        self.user = get_alphabetic_user_profiles(
            number_of_users=1, saved=True, with_corresponding_user=True
        )[0]
        self.existing_dating_entry = Dating.objects.create(
            user_profile=self.user,
            name="Test User",
            area=CZECHOSLOVAK_REGIONS[1][1],
            text="Zahrál bych si",
            email="test@example.com",
        )
        self.selenium.get(self.live_server_url)

    def navigate_to_dating(self, user_profile=None):
        if user_profile:
            return self.navigate_as_authenticated_user(
                user_profile,
                navigation_element=MainPage.NAVIGATION_DATING,
                expected_title="Seznamka",
            )
        else:
            self.selenium.find_element(
                By.XPATH, MainPage.NAVIGATION_DATING.value
            ).click()

    def navigate_to_dating_create(self, user_profile=None):
        self.navigate_to_dating(user_profile)
        self.selenium.find_element(
            By.XPATH, DatingListPage.CREATE_DATING_LINK.value
        ).click()

    def create_dating_entry(
        self,
        name,
        area,
        text,
        email=None,
        group=None,
        age=None,
        phone=None,
        mobile=None,
        experience=None,
    ):
        """Helper method to fill and submit dating entry form"""
        self.selenium.find_element(By.ID, DatingCreatePage.NAME_INPUT.value).send_keys(
            name
        )
        if email:
            self.selenium.find_element(
                By.ID, DatingCreatePage.EMAIL_INPUT.value
            ).send_keys(email)
        self.selenium.find_element(By.ID, DatingCreatePage.AREA_INPUT.value).send_keys(
            area
        )
        self.selenium.find_element(By.ID, DatingCreatePage.TEXT_INPUT.value).send_keys(
            text
        )

        if group:
            select = Select(
                self.selenium.find_element(By.ID, DatingCreatePage.GROUP_SELECT.value)
            )
            select.select_by_visible_text(group)
        if age:
            self.selenium.find_element(
                By.ID, DatingCreatePage.AGE_INPUT.value
            ).send_keys(age)
        if phone:
            self.selenium.find_element(
                By.ID, DatingCreatePage.PHONE_INPUT.value
            ).send_keys(phone)
        if mobile:
            self.selenium.find_element(
                By.ID, DatingCreatePage.MOBILE_INPUT.value
            ).send_keys(mobile)
        if experience:
            self.selenium.find_element(
                By.ID, DatingCreatePage.EXPERIENCE_INPUT.value
            ).send_keys(experience)

        self.selenium.find_element(
            By.XPATH, DatingCreatePage.SUBMIT_BUTTON.value
        ).click()

    def test_can_view_dating_list_anonymous(self):
        """Test that anonymous user can view dating list"""
        self.navigate_to_dating()
        text = self.selenium.find_element(By.XPATH, '//h1[@class="page-heading"]').text
        self.assertEquals("Seznamka", text)

        text = self.selenium.find_element(
            By.XPATH, DatingListPage.FIRST_TEXT.value
        ).text
        self.assertEquals(self.existing_dating_entry.text, text)
