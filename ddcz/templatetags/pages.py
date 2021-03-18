from django import template

register = template.Library()


@register.inclusion_tag("creative-pages/pagination-links.html")
def pagination(articles):
    return {
        "articles": articles,
    }
