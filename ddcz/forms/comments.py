from ..models.used.discussion import Phorum
from django import forms


class PhorumCommentForm(forms.Form):

    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )
