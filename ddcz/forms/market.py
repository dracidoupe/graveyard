from django import forms
from django.core.validators import EmailValidator
from django.utils.html import escape
from ddcz.models import Market
from ddcz.geo import CZECHOSLOVAK_REGIONS


class MarketForm(forms.ModelForm):
    mail = forms.EmailField(
        required=False,
        label="Email",
        validators=[EmailValidator(message="Zadejte platnou emailovou adresu")],
    )

    area = forms.ChoiceField(
        choices=CZECHOSLOVAK_REGIONS,
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

    def clean_text(self):
        text = self.cleaned_data["text"]
        return escape(text) if text else ""
