from enum import Enum
import socket

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.functional import classproperty

from playwright.sync_api import sync_playwright


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
    NAVIGATION_MARKET = '//*[@id="ddcz_nav_market"]'
    NAVIGATION_DATING = '//*[@id="ddcz_nav_dating"]'


class _PWElement:
    def __init__(self, locator):
        self._locator = locator

    @property
    def text(self):
        # inner_text waits for element to be visible and returns rendered text
        return self._locator.inner_text()

    def click(self):
        self._locator.click()

    def send_keys(self, text):
        # emulate Selenium's send_keys by filling/typing
        try:
            self._locator.fill("")
        except Exception:
            pass
        self._locator.type(str(text))

    def get_attribute(self, name):
        return self._locator.get_attribute(name)

    def submit(self):
        # Approximate submit by clicking the element; if inside a form, this triggers submit
        try:
            self._locator.click()
        except Exception:
            # Fallback: evaluate form submit
            self._locator.evaluate("el => el.form && el.form.submit()")


class _SeleniumLikeShim:
    def __init__(self, page):
        self._page = page

    def _select(self, selector):
        # If it looks like XPath, use XPath. Otherwise assume it's an element id.
        sel = selector.strip()
        if sel.startswith("//") or sel.startswith("/"):
            return self._page.locator(f"xpath={sel}")
        else:
            return self._page.locator(f"#{sel}")

    def get(self, url):
        self._page.goto(url)

    def find_element(self, by_or_selector, value=None):
        selector = value if value is not None else by_or_selector
        locator = self._select(selector)
        return _PWElement(locator.first)

    def find_elements(self, by_or_selector, value=None):
        selector = value if value is not None else by_or_selector
        locator = self._select(selector)
        return [_PWElement(loc) for loc in locator.all()]


class SeleniumTestCase(StaticLiveServerTestCase):
    # We are always connect to all interfaces
    # to simplify the local and CI setup
    host = "0.0.0.0"

    @classproperty
    def live_server_url(cls):
        return "http://%s:%s" % (
            getattr(settings, "TEST_LIVE_SERVER_HOST", None) or socket.gethostname(),
            cls.server_thread.port,
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Launch Playwright Chromium
        cls._playwright = sync_playwright().start()
        cls._browser = cls._playwright.chromium.launch(headless=True)
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        # Selenium-like interface for existing tests
        cls.selenium = _SeleniumLikeShim(cls._page)

        # Keep DEBUG consistent with original override behavior
        if not settings.DEBUG and getattr(settings, "OVERRIDE_SELENIUM_DEBUG", False):
            settings.DEBUG = True

        cls.main_page_nav = MainPage

    @classmethod
    def tearDownClass(cls):
        try:
            cls._context.close()
            cls._browser.close()
            cls._playwright.stop()
        finally:
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
        return self.selenium.find_element(enum.value)

    def els(self, enum):
        return self.selenium.find_elements(enum.value)

    def is_logged_in(self):
        return self.el(MainPage.BODY).get_attribute("data-logged-in") == "1"

    # Convenience for selecting <select> options by visible text or value
    def _to_selector(self, selector: str) -> str:
        sel = selector.strip()
        if sel.startswith("//") or sel.startswith("/"):
            return f"xpath={sel}"
        else:
            return f"#{sel}"

    def select_by_visible_text(self, element_selector: str, label: str):
        self._page.select_option(self._to_selector(element_selector), label=label)

    def select_by_value(self, element_selector: str, value: str):
        self._page.select_option(self._to_selector(element_selector), value=value)
