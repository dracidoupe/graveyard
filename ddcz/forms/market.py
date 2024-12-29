from django import forms
from django.core.validators import EmailValidator
from ddcz.models import Market


CZECH_REGIONS = [
    ("", "-- Vyberte kraj --"),
    ("Celá ČR", "Celá ČR"),
    ("Celá SR", "Celá SR"),
    # Czech Republic
    ("Praha", "Praha"),
    ("Středočeský", "Středočeský"),
    ("Jihočeský", "Jihočeský"),
    ("Plzeňský", "Plzeňský"),
    ("Karlovarský", "Karlovarský"),
    ("Ústecký", "Ústecký"),
    ("Liberecký", "Liberecký"),
    ("Královéhradecký", "Královéhradecký"),
    ("Pardubický", "Pardubický"),
    ("Vysočina", "Vysočina"),
    ("Jihomoravský", "Jihomoravský"),
    ("Olomoucký", "Olomoucký"),
    ("Zlínský", "Zlínský"),
    ("Moravskoslezský", "Moravskoslezský"),
    # Slovak Republic
    ("Bratislavský", "Bratislavský"),
    ("Trnavský", "Trnavský"),
    ("Trenčianský", "Trenčianský"),
    ("Nitrianský", "Nitrianský"),
    ("Žilinský", "Žilinský"),
    ("Banskobystrický", "Banskobystrický"),
    ("Prešovský", "Prešovský"),
    ("Košický", "Košický"),
]


class MarketForm(forms.ModelForm):
    mail = forms.EmailField(
        required=False,
        label="Email",
        validators=[EmailValidator(message="Zadejte platnou emailovou adresu")],
    )

    area = forms.ChoiceField(
        choices=CZECH_REGIONS,
        label="Kraj",
        required=True,
    )

    class Meta:
        model = Market
        fields = ["name", "mail", "group", "area", "phone", "mobile", "text"]
        labels = {
            "name": "Jméno",
            "mail": "Email",
            "group": "Sekce",
            "area": "Kraj",
            "phone": "Telefon",
            "mobile": "Mobil",
            "text": "Text inzerátu",
        }
