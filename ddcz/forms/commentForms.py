from django import forms
from django.http import HttpResponse
from ..models.used.discussion import Phorum


class PhorumCommentForm(forms.Form):
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )
    username = forms.HiddenInput()
