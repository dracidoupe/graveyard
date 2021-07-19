from datetime import datetime
from enum import Enum, unique
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..forms.comments import CommentAction
from ..forms.tavern import TavernPostForm, NoticeBoardForm, TavernTableAdminForm
from ..models import (
    TavernTable,
    TavernPost,
    TavernTableNoticeBoard,
    TavernTableVisitor,
    TavernBookmark,
    TavernAccessRights,
)
from ..tavern import (
    LIST_ALL,
    LIST_FAVORITE,
    SUPPORTED_LIST_STYLES_DISPLAY_NAME,
    get_tavern_table_list,
    bookmark_table,
    unbook_table,
    post_table_post,
)

from ..text import escape_user_input


@unique
class BookmarkActions(Enum):
    BOOK = "oblibit"
    UNBOOK = "neoblibit"


def handle_table_visit(view_func):
    """
    Check if the tavern table is accessible:
        * If not, redirect to the tavern table list
        * If yes, update visit time and attach common variables
    """

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        if "tavern_table_id" in kwargs:
            # TODO: room for optimization, could be pre-selected with visitor
            request.tavern_table = table = get_object_or_404(
                TavernTable, pk=kwargs["tavern_table_id"]
            )
            if table.is_user_access_allowed(user_profile=request.ddcz_profile):
                (
                    request.tavern_table.visitor,
                    created,
                ) = TavernTableVisitor.objects.get_or_create(
                    tavern_table=table,
                    user_profile=request.ddcz_profile,
                    defaults={"unread": 0, "visit_time": datetime.now()},
                )
                if not created:
                    request.tavern_table.visitor.visit_time = datetime.now()
                    request.tavern_table.visitor.save()

                # This will be in the future just inferred from the visitor, but for now, the normative
                # data is in the TavernBookmark, unfortunately
                table.is_bookmarked = (
                    TavernBookmark.objects.filter(
                        tavern_table=table, user_profile=request.ddcz_profile
                    ).count()
                    == 1
                )

                table.user_can_admin = table.is_admin(request.ddcz_profile)

                # Call the actual view function
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
@handle_table_visit
def table_posts(request, tavern_table_id):
    table = request.tavern_table
    user_can_post = table.is_user_write_allowed(user_profile=request.ddcz_profile)
    posts_page = request.GET.get("z_s", 1)

    if request.method == "POST":
        # Create new Post

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
                post_table_post(
                    tavern_table=table,
                    author_profile=request.ddcz_profile,
                    text=escape_user_input(post_form.cleaned_data["text"]),
                )
                return HttpResponseRedirect(request.get_full_path())

    else:
        if posts_page == 1:
            table.visitor.unread = 0
            table.visitor.save()
        post_form = TavernPostForm()

    return render(
        request,
        "tavern/posts.html",
        {
            "table": table,
            "posts_page": posts_page,
            "post_form": post_form,
            "user_can_post": user_can_post,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
@handle_table_visit
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
                    text=escape_user_input(post_form.cleaned_data["text"]),
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


@login_required
@require_http_methods(["GET"])
@handle_table_visit
def table_bookmark(request, tavern_table_id):
    table = request.tavern_table

    # TODO: The "Book" button should be a form and it should sent a POST request
    if "akce" not in request.GET:
        return HttpResponseBadRequest(
            "`akce` request parameter is mandatory for this endpoint"
        )
    try:
        action = BookmarkActions(request.GET["akce"])
    except ValueError:
        return HttpResponseBadRequest(
            f"Invalid parameter for `akce`: {request.GET['akce']}"
        )

    if action == BookmarkActions.BOOK:
        bookmark_table(user_profile=request.ddcz_profile, tavern_table=table)
    elif action == BookmarkActions.UNBOOK:
        unbook_table(user_profile=request.ddcz_profile, tavern_table=table)

    return HttpResponseRedirect(
        reverse("ddcz:tavern-posts", kwargs={"tavern_table_id": table.pk})
    )


@login_required
@require_http_methods(["GET", "POST"])
@handle_table_visit
def table_administration(request, tavern_table_id):
    table = request.tavern_table
    if not table.is_admin(request.ddcz_profile):
        return HttpResponseForbidden("Nemáte právo administrovat stůl.")

    if request.method == "POST":
        tavern_table_admin_form = TavernTableAdminForm(request.POST)
        if tavern_table_admin_form.is_valid():
            table.name = tavern_table_admin_form.cleaned_data["name"]
            table.description = tavern_table_admin_form.cleaned_data["description"]
            table.allow_rep = (
                "1" if tavern_table_admin_form.cleaned_data["allow_rep"] else "0"
            )
            table.public = (
                "1"
                if len(tavern_table_admin_form.cleaned_data["access_allowed"]) == 0
                else "0"
            )
            table.save()

            table.update_access_privileges(
                access_banned=tavern_table_admin_form.cleaned_data["access_banned"],
                access_allowed=tavern_table_admin_form.cleaned_data["access_allowed"],
                write_allowed=tavern_table_admin_form.cleaned_data["write_allowed"],
                assistant_admins=tavern_table_admin_form.cleaned_data[
                    "assistant_admins"
                ],
            )

            return HttpResponseRedirect(request.get_full_path())
    else:
        privileges = table.get_current_privileges_map()

        tavern_table_admin_form = TavernTableAdminForm(
            {
                "name": table.name,
                "description": table.description,
                "allow_rep": table.allow_rep == "1",
                "assistant_admins": ", ".join(
                    privileges[TavernAccessRights.ASSISTANT_ADMIN]
                ),
                "write_allowed": ", ".join(
                    privileges[TavernAccessRights.WRITE_ALLOWED]
                ),
                "access_allowed": ", ".join(
                    privileges[TavernAccessRights.ACCESS_ALLOWED]
                ),
                "access_banned": ", ".join(
                    privileges[TavernAccessRights.ACCESS_BANNED]
                ),
            }
        )

    return render(
        request,
        "tavern/table-admin.html",
        {
            "table": table,
            "admin_form": tavern_table_admin_form,
        },
    )
