from ddcz.models.used.users import UserProfile
import logging

from django.contrib.staticfiles.storage import staticfiles_storage
from django import template

logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag("users/level-star.html")
def level_star(user_profile, skin):
    if not user_profile or not skin:
        logger.error(
            f"Insufficient data to render level start: user_profile {user_profile}, skin {skin}"
        )

    level = user_profile.level or "0"
    return {
        "star_image_url": staticfiles_storage.url(
            "skins/%s/img/star-level-%s.svg" % (skin, level)
        ),
        "level": level,
    }


@register.filter
def nick_icon(nick):
    try:
        return UserProfile.objects.get(nick=nick).icon_url
    except:
        return ""


@register.filter
def nick_url(nick):
    try:
        return UserProfile.objects.get(nick=nick).profile_url
    except:
        return "#"
