from django import forms
from django.http import HttpResponse
from ..discussion import Phorum


class PhorumCommentaryForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'Comment--TextArea'}))
    username = forms.HiddenInput()

    @staticmethod
    def getPhorumObject(form, user, reputation=0):
        if form.is_valid():
            return Phorum(
                nickname=user.nick_uzivatele,
                email=user.email_uzivatele,
                text=form.cleaned_data["text"],
                reg=1,
                reputace=reputation,
                user=user
            )
