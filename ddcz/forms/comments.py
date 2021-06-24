from enum import Enum
from django import forms


class CommentAction(Enum):
    ADD = "a"
    DELETE = "d"


class PhorumCommentForm(forms.Form):
    post_type = forms.CharField(
        widget=forms.HiddenInput(attrs={"value": CommentAction.ADD.value})
    )
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )


class DeletePhorumCommentForm(forms.Form):
    post_type = forms.CharField(
        widget=forms.HiddenInput(attrs={"value": CommentAction.DELETE.value})
    )
    post_id = forms.CharField(widget=forms.HiddenInput)


class TavernPostForm(forms.Form):
    action = forms.CharField(
        widget=forms.HiddenInput(attrs={"value": CommentAction.ADD.value})
    )
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )
