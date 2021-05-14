from time import time
from enum import Enum
import logging

from django import forms
from django.forms import ModelForm
from django.contrib.auth import forms as authforms
from django.utils.safestring import mark_safe

from ..models import UserProfile, UzivateleCekajici

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    nick = forms.CharField(label="Nick", max_length=25)
    password = forms.CharField(
        label="Heslo", max_length=100, widget=forms.PasswordInput
    )


class PasswordResetForm(authforms.PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This is overridem from original form to use UserProfile instead of standard
        user model since that is normative for email storage.
        """

        user_profiles = UserProfile.objects.filter(email_uzivatele__iexact=email)

        users = tuple(
            list(
                up.user
                for up in user_profiles
                if up.user.has_usable_password() and up.user.is_active
            )
        )

        logger.info(
            "Selected users for password reset: %s"
            % ", ".join([str(u.pk) for u in users])
        )

        return users


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

    # Setting the data
    @classmethod
    def set_for_save(cls, data):
        data["datum"] = int(time())

        data["primluvy"] = 0
        data["patron"] = 0
        data["popis_text"] = cls.set_description(data)
        return data

    @staticmethod
    def set_description(data):
        popis = "1. " + data["duvod_registrace"] + "\n"
        popis += "2. " + data["odkud_znas_web"] + "\n"
        popis += "3. " + data["kamaradi_na_webu"] + "\n"
        popis += "4. \n"
        popis += "5. \n"
        return popis

    # Validations for the form
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
