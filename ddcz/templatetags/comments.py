from django.core.paginator import Paginator
from django import template

from ddcz.models import CreationComment, TavernPost

register = template.Library()

COMMENT_DEFAULT_LIMIT = 10


@register.filter
def commentTime(datetime):
    try:
        return datetime.strftime("%-d. %-m. %Y v %-H:%M:%S")
    except ValueError:
        return datetime.strftime("%d. %m. %Y v %H:%M:%S")


@register.inclusion_tag("discussions/creation-comments.html", takes_context=True)
def creation_comments(context, creative_page_slug, creation_pk):
    comments = CreationComment.objects.filter(
        foreign_table=creative_page_slug, foreign_id=creation_pk
    ).order_by("-date")

    paginator = Paginator(comments, COMMENT_DEFAULT_LIMIT)
    comments = paginator.get_page(context["comment_page"])

    return {
        "comments": comments,
        "user": context["user"],
        "skin": context["skin"],
        "creation_comment_form": context["creation_comment_form"],
        "display_comment_header": True,
    }


@register.inclusion_tag("discussions/creation-comments.html", takes_context=True)
def tavern_posts(context, tavern_table):
    comments = TavernPost.objects.filter(tavern_table=tavern_table).order_by("-date")

    paginator = Paginator(comments, COMMENT_DEFAULT_LIMIT)
    comments = paginator.get_page(context["posts_page"])

    return {"comments": comments, "user": context["user"], "skin": context["skin"]}
