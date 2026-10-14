from enum import Enum
from html import unescape

from django import forms

from ddcz.commonarticles import COMMON_ARTICLES_CREATIVE_PAGES
from ddcz.creations import RATING_DESCRIPTIONS
from ddcz.submissions import RATING_ABSTAIN
from ddcz.text import escape_user_input


class ReviewAction(Enum):
    APPROVE = "approve"
    REJECT = "reject"


ReviewAction.do_not_call_in_templates = True

RATING_CHOICES = [
    (rating, f"{rating} – {description}")
    for rating, description in RATING_DESCRIPTIONS.items()
    if rating < 6
] + [(RATING_ABSTAIN, "Vzdát se hlasování")]


class CommonArticleReview(forms.Form):
    name = forms.CharField(label="Název", max_length=255)
    abstract = forms.CharField(label="Anotace", max_length=255, required=False)
    section = forms.ChoiceField(label="Skupina")
    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(attrs={"cols": 100, "rows": 30}),
    )
    rating = forms.TypedChoiceField(
        label="Hodnocení redaktora",
        choices=RATING_CHOICES,
        coerce=int,
    )
    comment = forms.CharField(
        label="Komentář pod dílem",
        required=False,
        widget=forms.Textarea(attrs={"cols": 100, "rows": 5}),
    )

    def __init__(self, *args, creative_page_slug, **kwargs):
        super().__init__(*args, **kwargs)
        sections = list(COMMON_ARTICLES_CREATIVE_PAGES[creative_page_slug]["sections"])
        self.fields["section"].choices = [(s, s) for s in sections]

    @classmethod
    def from_article(cls, article):
        return cls(
            creative_page_slug=article.creative_page_slug,
            initial={
                "name": unescape(article.name),
                "abstract": unescape(article.abstract or ""),
                "section": article.section,
                "text": unescape(article.text),
                "rating": 3,
            },
        )

    def clean_name(self):
        return escape_user_input(self.cleaned_data["name"], newline_to_br=False)

    def clean_abstract(self):
        return escape_user_input(self.cleaned_data["abstract"], newline_to_br=False)

    def clean_text(self):
        return escape_user_input(self.cleaned_data["text"], newline_to_br=False)

    def save_to_article(self, article):
        article.name = self.cleaned_data["name"]
        article.abstract = self.cleaned_data["abstract"]
        article.section = self.cleaned_data["section"]
        article.text = self.cleaned_data["text"]
        article.save()


class CommonArticleRejection(forms.Form):
    reason = forms.CharField(
        label="Důvod zamítnutí",
        widget=forms.Textarea(attrs={"cols": 100, "rows": 5}),
    )
