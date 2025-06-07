from django import forms
from django.utils.html import escape
from ..models import Dating
from ..geo import CZECHOSLOVAK_REGIONS


class DatingForm(forms.ModelForm):
    area = forms.ChoiceField(
        choices=CZECHOSLOVAK_REGIONS,
        label="Kraj",
        required=True,
    )

    class Meta:
        model = Dating
        fields = [
            "name",
            "email",
            "group",
            "phone",
            "mobile",
            "age",
            "area",
            "experience",
            "text",
        ]

    def clean_text(self):
        text = self.cleaned_data["text"]
        return escape(text) if text else ""
