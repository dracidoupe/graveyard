from django import template
from django.http import request

register = template.Library()


@register.inclusion_tag("creative-pages/pagination-links.html")
def pagination(articles, per_page=False):
    return {"articles": articles, "per_page": per_page}
