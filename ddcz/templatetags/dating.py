from django import template

register = template.Library()

DATING_GROUP_MAP = {"hledam_pj": "Hledám PJe", "hledam_hrace": "Hledám hráče"}


@register.filter
def dating_group_map(key):
    try:
        return DATING_GROUP_MAP[key]
    except KeyError:
        return "Hledám"
