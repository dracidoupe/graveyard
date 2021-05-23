from ddcz.models.used.tavern import TavernTableVisitor
from datetime import date
from hashlib import md5
import logging
from zlib import crc32

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from ..commonarticles import (
    SLUG_NAME_TRANSLATION_FROM_CZ,
    COMMON_ARTICLES_CREATIVE_PAGES,
)
from ..models import (
    MARKET_SECTION_CHOICES,
    EditorArticle,
    Dating,
    Link,
    Market,
)

DEFAULT_LIST_SIZE = 10


# Get an instance of a logger
logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def links(request):
    item_list = Link.objects.filter(is_approved="a").order_by("-published")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "links/list.html", {"items": items})


@require_http_methods(["GET"])
def dating(request):
    item_list = Dating.objects.order_by("-published")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "dating/list.html", {"items": items})


@require_http_methods(["GET"])
def market(request):
    # TODO: Migrate to `-datum`, see https://github.com/dracidoupe/graveyard/issues/195
    item_list = Market.objects.order_by("-id")

    section = request.GET.get("sekce", None)
    if section:
        if not section in [i[0] for i in MARKET_SECTION_CHOICES]:
            raise Http404()

        item_list = item_list.filter(sekce=request.GET.get("sekce"))

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "market/list.html", {"items": items})


@require_http_methods(["GET"])
def editor_article(request, slug):
    article = get_object_or_404(EditorArticle, slug=slug)

    return render(
        request,
        "info/editor-article.html",
        {"article": article},
    )
