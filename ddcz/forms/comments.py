from django import forms


class PhorumCommentForm(forms.Form):

    post_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "a"}))
    text = forms.CharField(
        label="", widget=forms.Textarea(attrs={"class": "comment__textarea"})
    )


class DeletePhorumCommentForm(forms.Form):
    post_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "d"}))
    post_id = forms.CharField(widget=forms.HiddenInput)
