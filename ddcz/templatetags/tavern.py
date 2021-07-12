import logging

from django import template
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from ..html import encode_valid_html

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def tavern_table_name(listing_table, user_profile):
    show_link = listing_table.show_listing_link(user_profile)

    return format_html(
        '{}<span class="tavern-table-name{}">{}</span>{}&nbsp;[{}{}]',
        mark_safe(
            f'<a href="{reverse_lazy("ddcz:tavern-posts", kwargs={"tavern_table_id": listing_table.pk})}">'
        )
        if show_link
        else "",
        " tavern_table_name__unread"
        if listing_table.new_comments_no is not None
        and listing_table.new_comments_no > 0
        else "",
        mark_safe(encode_valid_html(listing_table.name)),
        mark_safe("</a>") if show_link else "",
        f"{listing_table.new_comments_no}/"
        if listing_table.new_comments_no is not None
        else "",
        listing_table.posts_no,
    )
