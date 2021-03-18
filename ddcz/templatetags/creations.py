import logging

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from ..creations import RATING_DESCRIPTIONS

logger = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag("creations/rating.html")
def creation_rating(rating, skin):
    rating = int(rating or 0)
    return {
        "rating_description": "Hodnocení: %s" % RATING_DESCRIPTIONS[round(rating)],
        "rating": range(rating),
        "skin": skin,
        "skin_rating_star_url": staticfiles_storage.url(
            "skins/%s/img/rating-star.gif" % skin
        ),
    }


@register.inclusion_tag("creations/author-display-link.html")
def author_display(creation_subclass):
    try:
        author = creation_subclass.author
        if not author:
            raise ValueError()

    except Exception:
        author_url = "#"
        author_name = "Neznámý"
        logger.exception(
            "Author not found, data migration error for creation %s" % creation_subclass
        )
    else:
        author_url = author.profile_url
        author_name = author.name

    return {"author_url": author_url, "author_name": author_name}


@register.simple_tag
def creation_canonical_url(page, creation):
    return page.get_creation_canonical_url(creation)


@register.filter
def articleTime(datetime):
    return datetime.strftime("%-d. %-m. %Y v %-H:%M")


@register.filter
def articleTimeAlternative(datetime):
    return datetime.strftime("%-H:%M, %-d. %-m. %Y")
