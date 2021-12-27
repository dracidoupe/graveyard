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

    class VisibilityChoices(Enum):
        FALSE = "Nezobrazovat na profilu"
        TRUE = "Zobrazit pro všechny"

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Zadej emailovou adresu", "id": "email"}
        ),
    )

    gender = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in SexChoices],
    )

    age = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={"placeholder": "Tvůj věk", "id": "age", "min": MIN_AGE, "max": 150}
        ),
    )

    name_given_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    name_family_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    email_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    gender_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    age_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    shire_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
    )

    icq_visibility = forms.ChoiceField(
        label="",
        widget=forms.Select(),
        choices=[(tag.name, tag.value) for tag in VisibilityChoices],
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
