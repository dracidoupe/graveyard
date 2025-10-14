from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ddcz.tests.test_ui.cases import SeleniumTestCase


class DragonPage(Enum):
    BODY = "//body"
    NAV_USERS = "//nav[@class='menu']//a[contains(text(), 'Uživatelé')]"
    USER_SEARCH_INPUT = "//input[@id='nick']"
    USER_SEARCH_SUBMIT = "//input[@type='submit'][@value='Vyhledat']"
    USER_INFO_TABLE = "//table"
    BAN_BUTTON = "//input[@value='Zablokovat uživatele']"
    UNBAN_BUTTON = "//input[@value='Odblokovat uživatele']"
    MESSAGE_SUCCESS = "//ul[@class='messages']/li[contains(@class, 'success')]"
    MESSAGE_ERROR = "//ul[@class='messages']/li[contains(@class, 'error')]"


class DragonSeleniumTestCase(SeleniumTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragon_page = DragonPage

    def dragon_login_as_staff(self, staff_profile, password):
        self.selenium.get(f"{self.live_server_url}/")

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, self.main_page_nav.LOGIN_USERNAME_INPUT.value)
            )
        )

        self.el(self.main_page_nav.LOGIN_USERNAME_INPUT).send_keys(
            staff_profile.user.username
        )
        self.el(self.main_page_nav.LOGIN_PASSWORD_INPUT).send_keys(password)
        self.el(self.main_page_nav.LOGIN_SUBMIT).click()

        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(
                By.XPATH, self.main_page_nav.BODY.value
            ).get_attribute("data-logged-in")
            == "1"
        )

        self.assertTrue(self.is_logged_in())

        self.selenium.get(f"{self.live_server_url}/sprava/")

    def el(self, enum):
        return self.selenium.find_element(By.XPATH, enum.value)

    def els(self, enum):
        return self.selenium.find_elements(By.XPATH, enum.value)
