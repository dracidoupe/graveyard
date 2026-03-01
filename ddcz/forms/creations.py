from django import forms

from ddcz.models import (
    CommonArticle,
    Monster,
    Skill,
    AlchemistTool,
    RangerSpell,
    WizardSpell,
    Item,
)


SYSTEM_FIELDS = [
    "author_nick",
    "author_mail",
    "is_published",
    "original_web",
    "original_web_mail",
    "rater_no",
    "rating_sum",
    "rating",
    "read",
    "printed",
    "published",
    "author",
]


class CommonArticleSubmitForm(forms.ModelForm):
    class Meta:
        model = CommonArticle
        exclude = SYSTEM_FIELDS + ["creative_page_slug", "section"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["abstract"].required = False


class MonsterSubmitForm(forms.ModelForm):
    class Meta:
        model = Monster
        exclude = SYSTEM_FIELDS


class SkillSubmitForm(forms.ModelForm):
    class Meta:
        model = Skill
        exclude = SYSTEM_FIELDS + ["voted"]


class AlchemistToolSubmitForm(forms.ModelForm):
    class Meta:
        model = AlchemistTool
        exclude = SYSTEM_FIELDS


class RangerSpellSubmitForm(forms.ModelForm):
    class Meta:
        model = RangerSpell
        exclude = SYSTEM_FIELDS


class WizardSpellSubmitForm(forms.ModelForm):
    class Meta:
        model = WizardSpell
        exclude = SYSTEM_FIELDS


class ItemSubmitForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = SYSTEM_FIELDS


# Maps model class name (lowercase) to form class
CREATION_SUBMIT_FORMS = {
    "commonarticle": CommonArticleSubmitForm,
    "monster": MonsterSubmitForm,
    "skill": SkillSubmitForm,
    "alchemisttool": AlchemistToolSubmitForm,
    "rangerspell": RangerSpellSubmitForm,
    "wizardspell": WizardSpellSubmitForm,
    "item": ItemSubmitForm,
}

# Model types that require file upload (not yet supported)
FILE_UPLOAD_MODELS = {"gallerypicture", "photo", "downloaditem", "quest"}
