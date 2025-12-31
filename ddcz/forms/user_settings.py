from enum import Enum

from django import forms


SHIRE_CHOICES = [
    ("", "-- Vyberte kraj --"),
    ("Praha", "Praha"),
    ("Středočeský kraj", "Středočeský kraj"),
    ("Budějovický kraj", "Budějovický kraj"),
    ("Plzeňský kraj", "Plzeňský kraj"),
    ("Karlovarský kraj", "Karlovarský kraj"),
    ("Ústecký kraj", "Ústecký kraj"),
    ("Liberecký kraj", "Liberecký kraj"),
    ("Královéhradecký kraj", "Královéhradecký kraj"),
    ("Pardubický kraj", "Pardubický kraj"),
    ("Kraj Vysočina", "Kraj Vysočina"),
    ("Brněnský kraj", "Brněnský kraj"),
    ("Olomoucký kraj", "Olomoucký kraj"),
    ("Moravskoslezský kraj", "Moravskoslezský kraj"),
    ("Zlínský kraj", "Zlínský kraj"),
    ("Bratislavský kraj", "Bratislavský kraj"),
    ("Trnavský kraj", "Trnavský kraj"),
    ("Trenčiansky kraj", "Trenčiansky kraj"),
    ("Nitriansky kraj", "Nitriansky kraj"),
    ("Žilinský kraj", "Žilinský kraj"),
    ("Banskobystrický kraj", "Banskobystrický kraj"),
    ("Prešovský kraj", "Prešovský kraj"),
    ("Košický kraj", "Košický kraj"),
]


class GenderChoices(Enum):
    M = "Muž"
    F = "Žena"


class PersonalSettingsForm(forms.Form):
    name_given = forms.CharField(
        label="Jméno",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )

    name_family = forms.CharField(
        label="Příjmení",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )

    email = forms.EmailField(
        label="E-mail",
        max_length=50,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-input"}),
    )

    gender = forms.ChoiceField(
        label="Pohlaví",
        choices=[(tag.name, tag.value) for tag in GenderChoices],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    shire = forms.ChoiceField(
        label="Kraj bydliště",
        choices=SHIRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    description = forms.CharField(
        label="Popis",
        max_length=255,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "rows": 5,
                "cols": 60,
            }
        ),
        help_text="Popis slouží k lepší identifikaci uživatele. Máte k dispozici asi 255 znaků.",
    )

    show_name_given = forms.BooleanField(
        label="Zobrazit jméno",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    show_name_family = forms.BooleanField(
        label="Zobrazit příjmení",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    show_email = forms.BooleanField(
        label="Zobrazit e-mail",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    show_gender = forms.BooleanField(
        label="Zobrazit pohlaví",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    show_age = forms.BooleanField(
        label="Zobrazit věk",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    show_shire = forms.BooleanField(
        label="Zobrazit kraj",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )

    @classmethod
    def from_user_profile(cls, user_profile):
        permissions = user_profile.public_listing_permissions
        gender_value = ""
        if user_profile.gender in ["Muž", "Mu\x9e"]:
            gender_value = "M"
        elif user_profile.gender in ["Žena", "®ena"]:
            gender_value = "F"

        return cls(
            initial={
                "name_given": user_profile.name_given,
                "name_family": user_profile.name_family,
                "email": user_profile.email,
                "gender": gender_value,
                "shire": user_profile.shire or "",
                "description": user_profile.description_raw or "",
                "show_name_given": permissions["name_given"],
                "show_name_family": permissions["name_family"],
                "show_email": permissions["email"],
                "show_gender": permissions["gender"],
                "show_age": permissions["age"],
                "show_shire": permissions["shire"],
            }
        )

    def save_to_user_profile(self, user_profile):
        user_profile.name_given = self.cleaned_data["name_given"]
        user_profile.name_family = self.cleaned_data["name_family"]
        user_profile.email = self.cleaned_data["email"]

        gender_map = {"M": "Muž", "F": "Žena"}
        user_profile.gender = gender_map.get(self.cleaned_data["gender"], "")

        user_profile.shire = self.cleaned_data["shire"]
        user_profile.description_raw = self.cleaned_data["description"]

        permissions = user_profile.public_listing_permissions
        new_permissions = [
            "1" if self.cleaned_data["show_name_given"] else "",
            "1" if self.cleaned_data["show_name_family"] else "",
            "1" if self.cleaned_data["show_email"] else "",
            "1" if permissions.get("icq", False) else "",
            "1" if self.cleaned_data["show_gender"] else "",
            "1" if self.cleaned_data["show_age"] else "",
            "1" if self.cleaned_data["show_shire"] else "",
            "1" if permissions.get("birthday", False) else "",
        ]
        user_profile.pii_display_permissions = ",".join(new_permissions)

        user_profile.save()

        if user_profile.user:
            user_profile.user.email = self.cleaned_data["email"]
            user_profile.user.save()
