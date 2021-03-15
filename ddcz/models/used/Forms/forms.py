from django import forms
from pprint import pprint


class PhorumCommentaryForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'Comment--TextArea'}))
    username = forms.HiddenInput()
