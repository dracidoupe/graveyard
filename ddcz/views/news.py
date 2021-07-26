from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..models import News

DEFAULT_LIST_SIZE = 10


@require_http_methods(["GET"])
@vary_on_cookie
def list(request):
    page = request.GET.get("z_s", 1)
    cache_key = "info:news:list"
    news = None

    if page == 1:
        news = cache.get(cache_key)

    if not news:
        news_list = News.objects.order_by("-date")
        paginator = Paginator(news_list, DEFAULT_LIST_SIZE)
        news = paginator.get_page(page)

        if page == 1:
            cache.set(cache_key, news)

    return render(request, "news/list.html", {"news": news})
