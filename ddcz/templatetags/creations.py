import logging

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from ..creations import RATING_DESCRIPTIONS
from ..models import CreationVote

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
            "skins/%s/img/rating-star.svg" % skin
        ),
        "dragon_url": staticfiles_storage.url(
            "skins/%s/img/rating-star-dragon.svg" % skin
        ),
    }


@register.inclusion_tag("creations/votes.html", takes_context=True)
def creation_votes(context, creative_page_slug, creation_pk):
    votes = CreationVote.get_creation_votes(
        creative_page_slug=creative_page_slug,
        creation_id=creation_pk,
    )

    return {"votes": votes, "user": context["user"], "skin": context["skin"]}


@register.inclusion_tag("creations/author-display-link.html")
def author_display(creation_subclass):
    author = getattr(creation_subclass, "author", None)
    if not author:
        author_url = "#"
        author_name = "Neznámý"
        logger.error(
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
    try:
        return datetime.strftime("%-d. %-m. %Y v %-H:%M")
    except ValueError:
        return datetime.strftime("%d. %m. %Y v %H:%M")


@register.filter
def czech_date(datetime):
    try:
        return datetime.strftime("%-d. %-m. %Y")
    except ValueError:
        return datetime.strftime("%d. %m. %Y")
