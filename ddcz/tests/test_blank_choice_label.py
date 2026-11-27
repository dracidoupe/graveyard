from django.test import SimpleTestCase

from ddcz.forms.dating import DatingForm
from ddcz.forms.market import MarketForm


class BlankChoiceLabelTestCase(SimpleTestCase):
    def test_section_select_blank_option_is_czech(self):
        for form_class in (DatingForm, MarketForm):
            with self.subTest(form=form_class.__name__):
                choices = dict(form_class().fields["group"].choices)
                self.assertEqual(str(choices[""]), "- Vyberte možnost -")
