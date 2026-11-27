import json
import logging

import sentry_sdk
from django.core import signals
from django.core.handlers.wsgi import WSGIHandler
from django.db import close_old_connections
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import path
from sentry_sdk.transport import Transport

from graveyard.sentry import get_sentry_options

logger = logging.getLogger(__name__)

SUBMITTED_PASSWORD = "tajne-heslo-z-formulare"
COOKIE_VALUE = "hodnota-z-cookie"
CLIENT_IP = "203.0.113.7"
PROXY_IP = "198.51.100.23"


class CapturingTransport(Transport):
    def __init__(self):
        super().__init__()
        self.events = []

    def capture_envelope(self, envelope):
        self.events.extend(
            item.payload.json for item in envelope.items if item.type == "event"
        )


def failing_view(request):
    password = request.POST["password"]
    logger.error("Zalogovaná chyba")
    raise RuntimeError(f"Pohled selhal, heslo má {len(password)} znaků")


urlpatterns = [path("selhani/", failing_view)]


@override_settings(ROOT_URLCONF=__name__, MIDDLEWARE=[])
class SentryReportingTestCase(SimpleTestCase):
    def setUp(self):
        self.transport = CapturingTransport()
        client = sentry_sdk.Client(
            dsn="https://public@sentry.invalid/1",
            transport=self.transport,
            default_integrations=False,
            auto_enabling_integrations=False,
            **get_sentry_options(),
        )
        self.addCleanup(client.close)

        signals.request_started.disconnect(close_old_connections)
        self.addCleanup(signals.request_started.connect, close_old_connections)

        environ = (
            RequestFactory()
            .post(
                "/selhani/?strana=2",
                data={"nick": "Trpaslík", "password": SUBMITTED_PASSWORD},
                HTTP_COOKIE=f"skin={COOKIE_VALUE}",
                HTTP_X_FORWARDED_FOR=PROXY_IP,
                REMOTE_ADDR=CLIENT_IP,
            )
            .environ
        )

        with sentry_sdk.isolation_scope() as scope:
            scope.set_client(client)
            with (
                self.assertLogs(logger, level="ERROR"),
                self.assertLogs("django.request", level="ERROR"),
            ):
                response = WSGIHandler()(environ, lambda *args, **kwargs: None)
                response.close()

        self.events = self.transport.events
        self.reported = json.dumps(self.events, ensure_ascii=False)

    def test_unhandled_exception_is_reported(self):
        exception_types = [
            value["type"]
            for event in self.events
            for value in event.get("exception", {}).get("values", [])
        ]
        self.assertEqual(exception_types, ["RuntimeError"])

    def test_logged_error_is_reported(self):
        logged_messages = [
            event["logentry"]["message"] for event in self.events if "logentry" in event
        ]
        self.assertEqual(logged_messages, ["Zalogovaná chyba"])

    def test_submitted_password_is_not_reported(self):
        self.assertNotIn(SUBMITTED_PASSWORD, self.reported)

    def test_cookies_are_not_reported(self):
        self.assertNotIn(COOKIE_VALUE, self.reported)

    def test_visitor_address_is_not_reported(self):
        self.assertNotIn(CLIENT_IP, self.reported)
        self.assertNotIn(PROXY_IP, self.reported)
