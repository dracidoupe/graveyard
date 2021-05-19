from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.http import (
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from ..tavern import (
    LIST_ALL,
    LIST_FAVORITE,
    SUPPORTED_LIST_STYLES_DISPLAY_NAME,
    get_tavern_table_list,
)


@login_required
@require_http_methods(["GET"])
def tavern(request):
    """
    Display list of Tavern Tables in a given style ("vypis") that user has access to.
    Supported styles:
        * Bookmarked tables ("oblibene"): Show only tables user has explicitly bookmarked
        TODO: * Active tables ("aktivni"): Show all tables except those in archive
        * All tables ("vsechny"): All tables
        TODO: * Search tables ("filter"): Show tables user has searched for
    """
    list_style = request.GET.get("vypis", None)
    if not list_style or list_style not in SUPPORTED_LIST_STYLES_DISPLAY_NAME:
        bookmarks = request.ddcz_profile.tavern_bookmarks.count()
        if bookmarks > 0:
            default_style = LIST_FAVORITE
        else:
            default_style = LIST_ALL
        return HttpResponseRedirect(
            f"{reverse('ddcz:tavern-list')}?vypis={default_style}"
        )

    tavern_tables = get_tavern_table_list(
        user_profile=request.ddcz_profile, list_style=list_style
    )

    return render(
        request,
        "tavern/list.html",
        {
            "tavern_tables": tavern_tables,
            "supported_list_styles": SUPPORTED_LIST_STYLES_DISPLAY_NAME,
            "current_list_style": list_style,
        },
    )
