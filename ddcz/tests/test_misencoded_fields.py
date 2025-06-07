from django.test import SimpleTestCase
from ddcz.models.magic import MisencodedCharField

class MisencodedFieldsTest(SimpleTestCase):
    def setUp(self):
        self.field = MisencodedCharField(max_length=100)

    def test_handles_normal_text(self):
        """Test that normal Czech text is handled correctly"""
        value = "Příliš žluťoučký kůň úpěl ďábelské ódy"
        processed = self.field.get_db_prep_value(value, None)
        self.assertEqual(
            processed.encode("latin2").decode("cp1250"),
            value
        )

    def test_handles_emoji_gracefully(self):
        """Test that emoji are handled gracefully by being stripped"""
        value = "Hello 👋 World 🌍"
        stripped_value = "Hello  World "
        processed = self.field.get_db_prep_value(value, None)
        decoded = processed.encode("latin2").decode("cp1250")

        self.assertEqual(decoded, stripped_value)

    def test_handles_special_characters_gracefully(self):
        """Test that special characters are handled gracefully"""
        value = "Test ♥ ☺ ♦"
        stripped_value = "Test   "
        processed = self.field.get_db_prep_value(value, None)
        decoded = processed.encode("latin2").decode("cp1250")
        self.assertEqual(decoded, stripped_value)