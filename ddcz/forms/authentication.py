import logging

from django import forms
from django.contrib.auth import forms as authforms

from ..models import UserProfile

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


class SignUpForm(forms.Form):

    SEX_CHOICES = {"0": "mužské", "1": "ženské"}
    GDPR_CHOICES = {
        "0": "S tímhle nemůžu souhlasit... To je moc, raději si najdu jiné město nebo zůstanu v lese. Měj se hezky, Endo, a díky za tvůj čas.",
        "1": "Jasně, souhlasím s tím, co všechno s tím, co jsem ti tady napsal, uděláte.",
    }

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
        choices=SEX_CHOICES.items(),
    )

    vek = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={"placeholder": "Tvůj věk", "id": "age"}),
    )

    duvod_registrace = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád patřil mezi nás?",
                "id": "motive",
            }
        ),
    )

    kamaradi_na_webu = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Znáš ve městě někoho mimo Virga?",
                "id": "web_friends",
                "class": "form-control",
            }
        ),
    )

    odkud_znas_web = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Odkud ses dozvěděl o existenci tohoto města (webu)?",
                "id": "source",
            }
        ),
    )

    gdpr = forms.ChoiceField(
        label="",
        widget=forms.Select(attrs={"id": "gdpr"}),
        choices=GDPR_CHOICES.items(),
    )
