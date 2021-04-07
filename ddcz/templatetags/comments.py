from django import template

from ddcz.models import CreationComment

register = template.Library()


@register.filter
def commentTime(datetime):
    return datetime.strftime("%-d. %-m. %Y v %-H:%M:%S")


@register.filter
def commentTimeAlternative(datetime):
    return datetime.strftime("%-H:%M:%S, %-d. %-m. %Y")


@register.inclusion_tag("discussions/creation-comments.html", takes_context=True)
def creation_comments(context, creative_page_slug, creation_pk):
    comments = CreationComment.objects.filter(
        cizi_tbl=creative_page_slug, id_cizi=creation_pk
    ).order_by("-datum")

    return {"comments": comments, "user": context["user"]}
