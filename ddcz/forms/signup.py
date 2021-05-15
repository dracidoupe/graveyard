from time import time
from enum import Enum

from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from ..models import UzivateleCekajici


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

    nick_uzivatele = forms.CharField(
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

    jmeno = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Křestní jméno", "id": "first_name"}
        ),
    )

    prijmeni = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Příjmení", "id": "last_name"}),
    )

    osloveni = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Oslovení", "id": "addressing"}),
    )

    pohlavi = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={"id": "sex"}),
        choices=[(tag.name, tag.value) for tag in SexChoices],
    )

    vek = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={"placeholder": "Tvůj věk", "id": "age"}),
    )

    duvod_registrace = forms.CharField(
        required=False,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád patřil mezi nás?",
                "id": "motive",
            }
        ),
    )

    kamaradi_na_webu = forms.CharField(
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

    odkud_znas_web = forms.CharField(
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
    primluvy = forms.CharField(required=False)
    datum = forms.CharField(required=False)
    popis_text = forms.CharField(required=False)

    class Meta:
        model = UzivateleCekajici
        fields = [
            "nick_uzivatele",
            "email",
            "jmeno",
            "prijmeni",
            "pohlavi",
            "osloveni",
            "datum",
            "patron",
            "primluvy",
            "popis_text",
        ]

    def clean(self):
        cdata = super(SignUpForm, self).clean()

        popis = "1. " + cdata["duvod_registrace"] + "\n"
        popis += "2. " + cdata["odkud_znas_web"] + "\n"
        popis += "3. " + cdata["kamaradi_na_webu"] + "\n"
        popis += "4. \n"
        popis += "5. \n"

        self.datum = int(time())
        self.popis_text = popis
        self.primluvy = 0
        self.patron = 0

        self.cleaned_data["datum"] = int(time())
        self.cleaned_data["popis_text"] = popis
        self.cleaned_data["primluvy"] = 0
        self.cleaned_data["patron"] = 0

    def clean_nick_uzivatele(self, *args, **kwargs):
        nick_uzivatele = self.cleaned_data.get("nick_uzivatele")
        bad_characters = []
        for char in self.FORBIDDEN_NICK_CHARACTERS:
            if char in nick_uzivatele:
                bad_characters.append(char)
        if len(bad_characters) > 0:
            raise forms.ValidationError(
                "Ve vašem nicku jsou následující zakázané znaky: ("
                + ", ".join(bad_characters)
                + ")."
            )
        return nick_uzivatele

    def clean_vek(self, *args, **kwargs):
        vek = self.cleaned_data.get("vek")
        if vek < self.MIN_AGE:
            raise forms.ValidationError(
                "Bohužel ti není " + self.MIN_AGE + " let. Zkus to, až budeš starší."
            )
        return vek

    def clean_pohlavi(self, *args, **kwargs):
        pohlavi = self.cleaned_data.get("pohlavi")
        if pohlavi not in ["M", "F"]:
            raise forms.ValidationError(
                "Bohužel toto pohlaví nám zůstává utajeno. Neplete si pohlaví s genderem?"
            )
        return "Muž" if pohlavi == "M" else "Žena"

    def clean_gdpr(self, *args, **kwargs):
        gdpr = self.cleaned_data.get("gdpr")
        if gdpr != "T":
            raise forms.ValidationError(
                "Pro registraci je nutné souhlasit se způsobem uchovávání a používání dat."
            )
        return 1 if gdpr == "T" else 0
