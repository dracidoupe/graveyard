from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from ..creations import RATING_DESCRIPTIONS

register = template.Library()

@register.inclusion_tag('creations/rating.html')
def creation_rating(rating, skin):
    return {
        'rating_description': "Hodnocení: %s" % RATING_DESCRIPTIONS[round(rating)],
        'rating': range(rating),
        'skin': skin,
        'skin_rating_star_url': staticfiles_storage.url("skins/%s/img/rating-star.gif" % skin),
    }

