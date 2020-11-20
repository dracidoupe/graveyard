from django.contrib.staticfiles.storage import staticfiles_storage

from django import template

register = template.Library()

@register.inclusion_tag('users/level-star.html')
def level_star(user_profile, skin):
    level = user_profile.level or '0'
    return {
        'star_image_url': staticfiles_storage.url("skins/%s/img/star-level-%s.gif" % (skin, level)),
        'level': level,
    }
