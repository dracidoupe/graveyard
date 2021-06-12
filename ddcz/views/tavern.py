from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import TavernTable, TavernPost
from ..tavern import (
    LIST_ALL,
    LIST_FAVORITE,
    SUPPORTED_LIST_STYLES_DISPLAY_NAME,
    get_tavern_table_list,
)


def table_accessible(view_func):
    """Check if the tavern table is accessible. If not, redirect to the tavern table list"""

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        if "tavern_table_id" in kwargs:
            request.tavern_table = table = get_object_or_404(
                TavernTable, pk=kwargs["tavern_table_id"]
            )
            if table.is_user_access_allowed(user_profile=request.ddcz_profile):
                response = view_func(request, *args, **kwargs)
                return response
        return HttpResponseRedirect(reverse("ddcz:tavern-list"))

    return _wrapped_view_func


@login_required
@require_http_methods(["GET"])
# It would make sense to call it just `list`, but that would make it shadow the build-in list function
def list_tables(request):
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


@login_required
@require_http_methods(["GET"])
@table_accessible
def table_posts(request, tavern_table_id):
    table = request.tavern_table
    return render(
        request,
        "tavern/posts.html",
        {
            "table": table,
            "posts_page": request.GET.get("z_s", 1),
        },
    )
