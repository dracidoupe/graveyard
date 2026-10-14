from django.test import SimpleTestCase

from ddcz.models.magic import MisencodedCharField
from ddcz.text import misencode


class MisencodedFieldsTest(SimpleTestCase):
    def setUp(self):
        self.field = MisencodedCharField(max_length=100)

    def test_handles_normal_text(self):
        """Test that normal Czech text is handled correctly"""
        value = "Příliš žluťoučký kůň úpěl ďábelské ódy"
        processed = self.field.get_db_prep_value(value, None)
        self.assertEqual(processed.encode("latin2").decode("cp1250"), value)

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

    def test_handles_c1_control_char_gracefully(self):
        """Test for control char causing DDCZ-2T"""
        value = "Keyd\x9ea"
        processed = self.field.get_db_prep_value(value, None)
        self.assertIsInstance(processed, str)
        self.assertEqual(processed.encode("latin2").decode("cp1250"), "Keyda")


class MisencodeFunctionTest(SimpleTestCase):
    def test_normal_czech_text_round_trips(self):
        value = "Příliš žluťoučký kůň úpěl ďábelské ódy"
        self.assertEqual(misencode(value).encode("latin2").decode("cp1250"), value)

    def test_c1_control_char_does_not_raise(self):
        self.assertEqual(misencode("Keyd\x9ea"), "Keyda")
        self.assertEqual(misencode("Mu\x9e"), "Mu")
