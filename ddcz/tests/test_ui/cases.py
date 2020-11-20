import socket

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.decorators import classproperty

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

class SeleniumTestCase(StaticLiveServerTestCase):
    # We are always connect to all interfaces
    # to simplify the local and CI setup
    host = '0.0.0.0'

    @classproperty
    def live_server_url(cls):
        return 'http://%s:%s' % (
            getattr(settings, 'TEST_LIVE_SERVER_HOST', None) or socket.gethostname(),
            cls.server_thread.port
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if not settings.SELENIUM_HUB_HOST:
            cls.selenium = webdriver.Chrome()
        else:
            cls.selenium = webdriver.Remote(
                desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                command_executor='http://%s:4444/wd/hub' % settings.SELENIUM_HUB_HOST
            )

        cls.selenium.implicitly_wait(settings.SELENIUM_IMPLICIT_WAIT)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
