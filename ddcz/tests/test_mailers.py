import warnings

from django.conf import settings
from django.core import mail
from django.test import SimpleTestCase


class MailersTestCase(SimpleTestCase):
    def test_default_mailer_is_configured(self):
        self.assertIn("default", settings.MAILERS)

    def test_mail_is_sent_through_default_mailer_without_deprecations(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            warnings.simplefilter("error", PendingDeprecationWarning)
            mail.send_mail(
                "Předmět", "Tělo zprávy", "noreply@example.com", ["user@example.com"]
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].sent_using, "default")
