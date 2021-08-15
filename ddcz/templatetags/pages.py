from django import template
from django.http import request

register = template.Library()


@register.inclusion_tag("creative-pages/pagination-links.html")
def pagination(articles, per_page=False):
    return {"articles": articles, "per_page": per_page}


@register.inclusion_tag("creative-pages/list-default.html")
def list_default(articles, page_slug=False, skin="light"):
    print("\n\n\n\n")
    return {"articles": articles, "creative_page_slug": page_slug, "skin": skin}
