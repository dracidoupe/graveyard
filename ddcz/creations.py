from enum import Enum

from django.apps import apps as global_apps
from django.db.models import Q

from ddcz.text import misencode

RATING_DESCRIPTIONS = {
    0: "Nepovedené",
    1: "Nic moc",
    2: "Něco to má do sebe",
    3: "Průměr",
    4: "Kvalita",
    5: "Geniální",
    6: "Vítěz soutěže",
}


class ApprovalChoices(Enum):
    APPROVED = "a"
    WAITING = "n"


# Explicit model name cache for environments where CreativePage.get_all_models() may not have fixtures loaded
CREATION_MODEL_NAMES = (
    "AlchemistTool",
    "CommonArticle",
    "DownloadItem",
    "GalleryPicture",
    "Item",
    "Monster",
    "Photo",
    "Quest",
    "RangerSpell",
    "Skill",
    "WizardSpell",
)


def transfer_creations(
    source_profile_id,
    target_profile_id,
    apps=None,
    creation_ids=None,
    delete_empty_source_author=True,
):
    """Transfer creations between users: for admin/data repair use only"""
    apps = apps or global_apps
    UserProfile = apps.get_model("ddcz", "UserProfile")
    Author = apps.get_model("ddcz", "Author")

    source_profile = UserProfile.objects.get(pk=source_profile_id)
    target_profile = UserProfile.objects.get(pk=target_profile_id)
    source_author = Author.objects.filter(user_id=source_profile_id).first()
    target_author = Author.objects.filter(user_id=target_profile_id).first()

    if target_author is None:
        raise ValueError(
            f"UserProfile {target_profile_id} has no Author row, not moving"
        )

    moved = {}
    for model_name in CREATION_MODEL_NAMES:
        Model = apps.get_model("ddcz", model_name)

        matches = Q(author_nick=misencode(source_profile.nick))
        if source_author is not None:
            matches |= Q(author=source_author)

        queryset = Model.objects.filter(matches)
        if creation_ids is not None:
            queryset = queryset.filter(pk__in=creation_ids.get(model_name, []))

        moved_pks = sorted(queryset.values_list("pk", flat=True))
        if not moved_pks:
            continue

        queryset.update(
            author=target_author,
            author_nick=target_profile.nick,
            author_mail=target_profile.email,
        )
        moved[model_name] = moved_pks

    if delete_empty_source_author and source_author is not None:
        still_has_creations = any(
            apps.get_model("ddcz", model_name)
            .objects.filter(author=source_author)
            .exists()
            for model_name in CREATION_MODEL_NAMES
        )
        # Delete author profile and let it be recreated once they add something,
        # otherwise weird empty sections in the profile
        if not still_has_creations:
            source_author.delete()

    return moved
