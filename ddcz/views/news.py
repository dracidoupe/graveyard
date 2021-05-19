from hashlib import md5
from zlib import crc32

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve, Resolver404
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..models import News

DEFAULT_LIST_SIZE = 10


@require_http_methods(["GET"])
@vary_on_cookie
def index(request):
    page = request.GET.get("z_s", 1)
    cache_key = "info:news:list"
    news = None

    if page == 1:
        news = cache.get(cache_key)

    if not news:
        news_list = News.objects.order_by("-datum")
        paginator = Paginator(news_list, DEFAULT_LIST_SIZE)
        news = paginator.get_page(page)

        if page == 1:
            cache.set(cache_key, news)

    return render(request, "news/list.html", {"news": news})
