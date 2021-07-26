from datetime import timedelta
from itertools import chain

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..creations import ApprovalChoices
from ..models import News, CreativePage

DEFAULT_LIST_SIZE = 10
NEWSFEED_OLDEST_ARTICLE_INTERVAL = timedelta(weeks=26)
NEWSFEED_MAX_ITEMS = 20


@require_http_methods(["HEAD", "GET"])
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


# @require_http_methods(["HEAD", "GET"])
# @vary_on_cookie
def newsfeed(request):
    min_date = timezone.now() - NEWSFEED_OLDEST_ARTICLE_INTERVAL
    pages = CreativePage.get_all_models()

    # This could have been a simple list comprehension. But for a reason unknown to me,
    # list(queryset) returns 'QuerySet' object has no attribute 'method', whereas iterating
    # over it works fine, as well as [a for a in queryset] list comprehension
    # Maybe try out again once we upgrade to newest Django
    articles = []
    for page in pages:
        model = page["model"]
        query = model.objects.filter(
            is_published=ApprovalChoices.APPROVED.value, published__gte=min_date
        ).order_by("-published")
        if model.__name__ == "CommonArticle":
            query = query.filter(creative_page_slug=page["page"].slug)
        query = query[0:NEWSFEED_MAX_ITEMS]
        for creation in query:
            creation.creative_page = page["page"]
            articles.append(creation)
    articles.sort(key=lambda article: article.published, reverse=True)

    return render(request, "news/newsfeed.html", {"articles": articles})
