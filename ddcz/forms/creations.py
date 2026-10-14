from django import forms

from ddcz.commonarticles import COMMON_ARTICLES_CREATIVE_PAGES
from ddcz.text import escape_user_input


class CommonArticleSubmissionForm(forms.Form):
    name = forms.CharField(label="Název", max_length=255)
    abstract = forms.CharField(
        label="Anotace",
        max_length=255,
        required=False,
        help_text="Krátce o tom, o čem příspěvek bude",
    )
    section = forms.ChoiceField(label="Skupina")
    text = forms.CharField(label="Text", widget=forms.Textarea)

    def __init__(self, *args, creative_page_slug, **kwargs):
        super().__init__(*args, **kwargs)
        sections = COMMON_ARTICLES_CREATIVE_PAGES[creative_page_slug]["sections"]
        self.fields["section"].choices = [(s, s) for s in sections]

    def clean_name(self):
        return escape_user_input(self.cleaned_data["name"], newline_to_br=False)

    def clean_abstract(self):
        return escape_user_input(self.cleaned_data["abstract"], newline_to_br=False)

    def clean_text(self):
        return escape_user_input(self.cleaned_data["text"], newline_to_br=False)
