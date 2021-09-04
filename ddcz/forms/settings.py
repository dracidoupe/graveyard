from time import time
from enum import Enum

from django import forms
from django.forms import ModelForm
from django.http import request
from django.utils.safestring import mark_safe

from ..models import UserProfile


class SettingsForm(ModelForm):

    MIN_AGE = 13

    class SexChoices(Enum):
        M = "mužské"
        F = "ženské"

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Zadej emailovou adresu", "id": "email"}
        ),
    )

    gender = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={"id": "sex"}),
        choices=[(tag.name, tag.value) for tag in SexChoices],
    )

    age = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={"placeholder": "Tvůj věk", "id": "age", "min": MIN_AGE, "max": 150}
        ),
    )

    description_raw = forms.CharField(required=False, label="", widget=forms.Textarea())

    class Meta:
        model = UserProfile
        fields = [
            "email",
            "name_given",
            "name_family",
            "age",
            "shire",
            "gender",
            "icq",
            "description_raw",
        ]
