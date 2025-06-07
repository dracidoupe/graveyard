from django import forms

from .comments import CommentAction
from ..text import misencode
from ..models import UserProfile


class TavernPostForm(forms.Form):
    action = forms.CharField(
        widget=forms.HiddenInput(attrs={"value": CommentAction.ADD.value})
    )
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )


class NoticeBoardForm(forms.Form):
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )


class TavernTableAdminForm(forms.Form):
    """
    Administration form for changing tavern table attributes as well as access privileges.

    BIG FAT WARNING: User enters user nicknames, but fields are normalized to UserProfile.ids
    """

    name = forms.CharField(label="Jméno")
    description = forms.CharField(label="Popis")
    assistant_admins = forms.CharField(label="Pomocní správci", required=False)
    write_allowed = forms.CharField(label="Zápis povolen", required=False)
    access_allowed = forms.CharField(label="Vstup povolen", required=False)
    access_banned = forms.CharField(label="Vstup zakázán", required=False)
    allow_rep = forms.BooleanField(label="Povolit reputaci", required=False)

    def get_verified_profile_ids(self, nicknames):
        if not nicknames:
            return []

        invalid_nicknames = set([])
        verified_profile_ids = set([])

        for nick in nicknames.split(","):
            nick = nick.strip()
            try:
                verified_profile_ids.add(
                    UserProfile.objects.values("id").get(nick=misencode(nick))["id"]
                )
            except UserProfile.DoesNotExist:
                invalid_nicknames.add(nick)

        if len(invalid_nicknames):
            raise forms.ValidationError(
                f"Následující přezdívky nebyly nalezeny: {', '.join(invalid_nicknames)}"
            )
        else:
            return list(verified_profile_ids)

    def clean_allow_rep(self):
        rep = self.cleaned_data.get("allow_rep", False)
        if rep:
            return "1"
        else:
            return "0"

    def clean_assistant_admins(self):
        return self.get_verified_profile_ids(
            self.cleaned_data.get("assistant_admins", None)
        )

    def clean_write_allowed(self):
        return self.get_verified_profile_ids(
            self.cleaned_data.get("write_allowed", None)
        )

    def clean_access_allowed(self):
        return self.get_verified_profile_ids(
            self.cleaned_data.get("access_allowed", None)
        )

    def clean_access_banned(self):
        return self.get_verified_profile_ids(
            self.cleaned_data.get("access_banned", None)
        )
