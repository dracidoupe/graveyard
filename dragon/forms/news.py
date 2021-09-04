from django import forms
from django.core.validators import MinLengthValidator

from ddcz.notifications import Audience


class News(forms.Form):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"class": "comment__textarea", "cols": 80, "rows": 30},
        ),
        validators=[MinLengthValidator(80)],
    )
    audience = forms.ChoiceField(
        choices=((i.name, i.value) for i in Audience), label="Komu poslat e-mail"
    )
