import os
import subprocess
from enum import Enum
import json
import platform
import socket
import sys
import tempfile
import urllib.request
import zipfile

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.functional import classproperty

from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By


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


class SeleniumTestCase(StaticLiveServerTestCase):
    # We are always connect to all interfaces
    # to simplify the local and CI setup
    host = "0.0.0.0"

    def __init__(self, *args, **kwargs):
        # Only check for chrome/driver locally, we do trust CI pipeline to set this up correctly
        if not os.environ.get("SERVER_CI", False) == "true":
            self.check_chromedriver()

        super().__init__(*args, **kwargs)

        if not settings.DEBUG and settings.OVERRIDE_SELENIUM_DEBUG:
            settings.DEBUG = True

        self.main_page_nav = MainPage

    def check_chromedriver(self):
        chrome_version = get_local_chrome_version()
        if not chrome_version:
            raise ValueError(
                "Could not determine local Chrome version. If you want to check with another browser, please fix this method"
            )

        chromedriver_version = get_local_chromedriver_version()
        download_new = True
        if not chromedriver_version:
            print("Chromedriver not found.")
        elif not chromedriver_version.startswith(chrome_version.rsplit(".", 1)[0]):
            print(
                f"Chromedriver version {chromedriver_version} is incompatible with Chrome version {chrome_version}."
            )
        else:
            download_new = False
        if download_new:
            print(
                "ChromeDriver is incompatible or not installed. Fetching compatible version..."
            )
            url = fetch_compatible_chromedriver(chrome_version)
            if url:
                download_path = tempfile.gettempdir()
                download_and_extract_chromedriver(url, download_path)
            else:
                print("Could not find compatible ChromeDriver version.")

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
                # desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                command_executor="http://%s:4444/wd/hub" % settings.SELENIUM_HUB_HOST,
                options=ChromiumOptions(),
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
        return self.selenium.find_element(By.XPATH, enum.value)

    def els(self, enum):
        return self.selenium.find_elements(By.XPATH, enum.value)

    def is_logged_in(self):
        return self.el(MainPage.BODY).get_attribute("data-logged-in") == "1"


def get_local_chrome_version():
    if sys.platform == "darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif sys.platform == "win32":
        chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    else:
        chrome_path = "google-chrome"

    try:
        result = subprocess.run(
            [chrome_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        version = result.stdout.decode("utf-8").strip().split()[-1]
        return version
    except Exception as e:
        print(f"Error getting local Chrome version: {e}")
        return None


def get_local_chromedriver_version():
    try:
        result = subprocess.run(
            ["chromedriver", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        version = result.stdout.decode("utf-8").strip().split(" ")[1]
        return version
    except Exception as e:
        print(f"Error getting local ChromeDriver version: {e}")
        return None


def fetch_compatible_chromedriver(version):
    system = platform.system()
    machine = platform.machine()

    platform_key = None
    if system == "Windows":
        platform_key = "win32" if machine.endswith("32") else "win64"
    elif system == "Darwin":
        platform_key = "mac-arm64" if machine == "arm64" else "mac-x64"
    elif system == "Linux":
        platform_key = "linux64"

    url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise ValueError("Failed to fetch ChromeDriver versions.")

        data = json.loads(response.read().decode())
        data["versions"].sort(key=lambda x: x["version"], reverse=True)
        for entry in data["versions"]:
            if entry[
                "version"
            ].startswith(
                ".".join(
                    version.split(".")[:-1]
                )  # ignore the last minor version since not all are released, but they are compatible
            ):
                for download_option in entry["downloads"]["chromedriver"]:
                    if download_option["platform"] == platform_key:
                        return download_option["url"]

        raise ValueError(f"Compatible chromedriver for version {version} not found.")


def download_and_extract_chromedriver(url, download_path):
    local_filename = os.path.basename(url)
    local_path = os.path.join(download_path, local_filename)
    urllib.request.urlretrieve(url, local_path)

    extract_dir = tempfile.mkdtemp()

    with zipfile.ZipFile(local_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    os.remove(local_path)

    chromedriver_dir = os.path.join(extract_dir, os.listdir(extract_dir)[0])
    extracted_chromedriver_path = os.path.join(chromedriver_dir, "chromedriver")

    if not os.path.exists(extracted_chromedriver_path):
        raise ValueError(
            f"Could not find chromedriver in extracted directory {extracted_chromedriver_path}"
        )
    if sys.platform != "win32":
        chromedriver_path = "/usr/local/bin/chromedriver"
        if (
            input(
                f"Do you want to move new downloaded chromedriver version to '{chromedriver_path}'? (type y to confirm): "
            )
            .strip()
            .lower()
            == "y"
        ):
            os.rename(extracted_chromedriver_path, chromedriver_path)
            os.chmod(chromedriver_path, 755)
        else:
            print(
                f"Chromedriver is located in {extracted_chromedriver_path}, please install it manually."
            )
    else:
        raise NotImplementedError(
            "Windows not supported for this, please check the code around this and write your own support :) "
        )
        # os.rename(chromedriver_path, "C:\\Windows\\chromedriver.exe")
