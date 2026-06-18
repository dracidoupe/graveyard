from django.test import TestCase
from ddcz.models import Author


class TestAuthorMigrationError(TestCase):
    def test_name_logs_warning_for_missing_display_name(self):
        author = Author.objects.create(
            author_type=Author.WEBSITE_TYPE,
            website="",
        )
        # This should trigger the logger.warning
        with self.assertLogs("ddcz.models.used.creations", level="WARNING") as cm:
            name = author.name
            self.assertEqual("Neznámý", name)
            self.assertTrue(
                any("MIGRATION_ERROR no display_name" in output for output in cm.output)
            )

    def test_name_logs_warning_for_anonymous_missing_display_name(self):
        author = Author.objects.create(
            author_type=Author.ANONYMOUS_USER_TYPE,
            anonymous_user_nick="",
        )
        with self.assertLogs("ddcz.models.used.creations", level="WARNING") as cm:
            name = author.name
            self.assertEqual("Neznámý", name)
            self.assertTrue(
                any("MIGRATION_ERROR no display_name" in output for output in cm.output)
            )
