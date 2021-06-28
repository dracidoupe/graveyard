from datetime import datetime
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..forms.comments import TavernPostForm, CommentAction, NoticeBoardForm
from ..models import TavernTable, TavernPost, TavernTableNoticeBoard
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
@require_http_methods(["GET", "POST"])
@table_accessible
def table_posts(request, tavern_table_id):
    table = request.tavern_table
    user_can_post = table.is_user_write_allowed(user_profile=request.ddcz_profile)

    if request.method == "POST":
        # if request.POST["post_type"] == CommentAction.DELETE.value:
        #     try:
        #         Phorum.objects.get(
        #             id=request.POST["post_id"],
        #             nickname=request.user.profile.nick,
        #         ).delete()
        #     except Phorum.DoesNotExist as e:
        #         messages.error(request, "Zprávu se nepodařilo smazat.")
        #
        if (
            request.POST.get("action", None) == CommentAction.ADD.value
            and user_can_post
        ):
            post_form = TavernPostForm(request.POST)
            if post_form.is_valid():
                TavernPost.objects.create(
                    tavern_table=table,
                    text=post_form.cleaned_data["text"],
                    reputation=0,
                    user=request.ddcz_profile,
                    author_nick=request.ddcz_profile.nick,
                    date=datetime.now(),
                )
            return HttpResponseRedirect(request.get_full_path())

    else:
        post_form = TavernPostForm()

    return render(
        request,
        "tavern/posts.html",
        {
            "table": table,
            "posts_page": request.GET.get("z_s", 1),
            "post_form": post_form,
            "user_can_post": user_can_post,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
@table_accessible
def notice_board(request, tavern_table_id):
    table = request.tavern_table
    user_can_update_notice_board = table.is_notice_board_update_allowed(
        user_profile=request.ddcz_profile
    )

    try:
        board = TavernTableNoticeBoard.objects.get(tavern_table=table)
    except TavernTableNoticeBoard.DoesNotExist:
        board = None

    if request.method == "POST":
        if not user_can_update_notice_board:
            return HttpResponseForbidden("Nemáte právo upravit nástěnku.")

        post_form = NoticeBoardForm(request.POST)
        if post_form.is_valid():
            if board:
                board.text = post_form.cleaned_data["text"]
                board.changed_at = datetime.now()
                board.change_author_nick = request.ddcz_profile.nick
                board.save()
            else:
                TavernTableNoticeBoard.objects.create(
                    tavern_table=table,
                    table_name=table.name,
                    text=post_form.cleaned_data["text"],
                    changed_at=datetime.now(),
                    change_author_nick=request.ddcz_profile.nick,
                )

            return HttpResponseRedirect(request.get_full_path())
    else:
        if board:
            post_form = NoticeBoardForm(initial={"text": board.text})
        else:
            post_form = NoticeBoardForm()

    return render(
        request,
        "tavern/notice-board.html",
        {
            "table": table,
            "notice_board": board,
            "post_form": post_form,
            "user_can_update_notice_board": user_can_update_notice_board,
        },
    )
