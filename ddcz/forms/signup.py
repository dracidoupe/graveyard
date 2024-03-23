from time import time
from enum import Enum

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from ..models import AwaitingRegistration


class SignUpForm(ModelForm):
    MIN_AGE = 13

    class SexChoices(Enum):
        M = "mužské"
        F = "ženské"

    class GdprChoices(Enum):
        F = mark_safe(
            "S tímhle nemůžu souhlasit&hellip; To je moc, raději si najdu jiné Město nebo zůstanu v lese. Měj se hezky, Endo, a díky za tvůj čas."
        )
        T = "Jasně, souhlasím se vším!"

    FORBIDDEN_NICK_CHARACTERS = (
        "@",
        "_",
        "%",
        '"',
        "'",
        "/",
        "\\",
        "!",
        "#",
        "$",
        "^",
        "&",
        "*",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        ":",
        ";",
        "=",
        "+",
        "?",
        "|",
        ",",
        "~",
    )

    nick = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Zadej svůj nick", "id": "nickname"}
        ),
    )

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Zadej emailovou adresu", "id": "email"}
        ),
    )

    name_given = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Křestní jméno", "id": "first_name"}
        ),
    )

    name_family = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Příjmení", "id": "last_name"}),
    )

    salutation = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Oslovení", "id": "addressing"}),
    )

    gender = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={"id": "sex"}),
        choices=[(tag.name, tag.value) for tag in SexChoices],
    )

    age = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={"placeholder": "Tvůj věk", "id": "age", "min": 10, "max": 150}
        ),
    )

    motive = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád patřil mezi nás?",
                "id": "motive",
            }
        ),
    )

    registered_friends = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Znáš ve Městě někoho mimo Virga?",
                "id": "web_friends",
                "class": "form-control",
            }
        ),
    )

    source = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Odkud ses dozvěděl o existenci tohoto Města (webu)?",
                "id": "source",
            }
        ),
    )

    gdpr = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={"id": "gdpr"}),
        choices=[(tag.name, tag.value) for tag in GdprChoices],
    )

    patron = forms.CharField(required=False)
    supporters = forms.CharField(required=False)
    date = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = AwaitingRegistration
        fields = [
            "nick",
            "email",
            "name_given",
            "name_family",
            "gender",
            "salutation",
            "date",
            "patron",
            "supporters",
            "description",
        ]

    def clean(self):
        cdata = super(SignUpForm, self).clean()

        popis = "1. " + cdata["motive"] + "\n"
        popis += "2. " + cdata["source"] + "\n"
        popis += "3. " + cdata["supporters"] + "\n"
        popis += "4. \n"
        popis += "5. \n"

        self.date = int(time())
        self.description = popis
        self.supporters = 0
        self.patron = 0

        self.cleaned_data["date"] = int(time())
        self.cleaned_data["description"] = popis
        self.cleaned_data["supporters"] = 0
        self.cleaned_data["patron"] = 0

    def clean_nick(self, *args, **kwargs):
        nick = self.cleaned_data.get("nick")
        bad_characters = []
        for char in self.FORBIDDEN_NICK_CHARACTERS:
            if char in nick:
                bad_characters.append(char)
        if len(bad_characters) > 0:
            raise forms.ValidationError(
                "Ve vašem nicku jsou následující zakázané znaky: ("
                + ", ".join(bad_characters)
                + ")."
            )
        return nick

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data.get("age")
        if age < self.MIN_AGE:
            raise forms.ValidationError(
                f"Bohužel ti není {self.MIN_AGE} let. Zkus to, až budeš starší"
            )
        return age

    def clean_gender(self, *args, **kwargs):
        gender = self.cleaned_data.get("gender")
        if gender not in ["M", "F"]:
            raise forms.ValidationError(
                "Bohužel toto pohlaví nám zůstává utajeno. Neplete si pohlaví s genderem?"
            )
        return "Muž" if gender == "M" else "Žena"

    def clean_gdpr(self, *args, **kwargs):
        gdpr = self.cleaned_data.get("gdpr")
        if gdpr != "T":
            raise forms.ValidationError(
                "Pro registraci je nutné souhlasit se způsobem uchovávání a používání dat."
            )
        return 1 if gdpr == "T" else 0
