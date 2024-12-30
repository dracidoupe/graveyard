import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from ..models import (
    Market,
    UserProfile,
    Dating,
    Link,
    EditorArticle,
    MARKET_SECTION_CHOICES,
)
from ..forms.market import MarketForm

DEFAULT_LIST_SIZE = 10


# Get an instance of a logger
logger = logging.getLogger(__name__)


@require_http_methods(["HEAD", "GET"])
def links(request):
    item_list = Link.objects.filter(is_approved="a").order_by("-published")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "links/list.html", {"items": items})


@require_http_methods(["HEAD", "GET"])
def dating(request):
    item_list = Dating.objects.order_by("-published")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "dating/list.html", {"items": items})


@require_http_methods(["HEAD", "GET"])
def market(request):
    item_list = Market.objects.order_by("-created")

    section = request.GET.get("sekce", None)
    if section:
        if section not in [i[0] for i in MARKET_SECTION_CHOICES]:
            raise Http404()

        item_list = item_list.filter(group=request.GET.get("sekce"))

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "market/list.html", {"items": items})


@require_http_methods(["HEAD", "GET"])
def editor_article(request, slug):
    article = get_object_or_404(EditorArticle, slug=slug)

    return render(
        request,
        "info/editor-article.html",
        {"article": article},
    )


@require_http_methods(["HEAD", "GET"])
def web_authors_and_editors(request):
    # FIXME: Have this in db/config file
    TRIBUNE_ID = 2244

    hall_of_fame = [
        {
            "user_profile": UserProfile.objects.get(nick="James Timqui"),
            "role": "programátor",
        },
        {
            "user_profile": UserProfile.objects.get(nick="Alcator"),
            "role": "programátor",
        },
        {
            "user_profile": UserProfile.objects.get(nick="Legar"),
            "role": "programátor",
        },
        {
            "user_profile": UserProfile.objects.get(nick="deshi"),
            "role": "tribun",
        },
        {
            "user_profile": UserProfile.objects.get(nick="Igi"),
            "role": "tribun",
        },
        {
            "user_profile": UserProfile.objects.get(nick="Suk"),
            "role": "tribun",
        },
        {
            "user_profile": UserProfile.objects.get(nick="Nathaka"),
            "role": "tribun",
        },
        {
            "user_profile": UserProfile.objects.get(nick="kamerask"),
            "role": "tribun",
        },
    ]

    return render(
        request,
        "info/web-authors-and-editors.html",
        {
            "tribune": UserProfile.objects.get(pk=TRIBUNE_ID),
            "famous_users": hall_of_fame,
        },
    )


def market_create(request):
    if request.method == "POST":
        form = MarketForm(request.POST)
        if form.is_valid():
            market_item = form.save(commit=False)
            market_item.user_profile = request.ddcz_profile
            form.save()
            return redirect("ddcz:market")
    else:
        form = MarketForm()

    return render(request, "market/create.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def market_delete(request, id):
    market_item = get_object_or_404(Market, id=id)
    if market_item.user_profile == request.ddcz_profile:
        market_item.delete()
    return redirect("ddcz:market")
