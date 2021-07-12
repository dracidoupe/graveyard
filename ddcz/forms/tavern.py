from django import forms

from ddcz.forms.comments import CommentAction


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
    name = forms.CharField(label="Jméno")
    description = forms.CharField(label="Popis")
    assistant_admins = forms.CharField(label="Pomocní správci", required=False)
    write_allowed = forms.CharField(label="Zápis povolen", required=False)
    access_allowed = forms.CharField(label="Vstup povolen", required=False)
    access_banned = forms.CharField(label="Vstup zakázán", required=False)
    allow_rep = forms.BooleanField(label="Povolit reputaci", required=False)
