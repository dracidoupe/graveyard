from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from .commonarticles import SLUG_NAME_TRANSLATION_FROM_CZ , COMMON_ARTICLES_CREATIVE_PAGES

from .models import CommonArticles, News

VALID_SKINS = ['light', 'dark']

def index(request):
    news = News.objects.order_by('-datum')[:5]
    return render(request, 'news/list.html', {'news': news})


def common_articles(request, creative_page_slug):
    try:
        en_slug = SLUG_NAME_TRANSLATION_FROM_CZ[creative_page_slug]
    except KeyError:
        raise Http404()

    articles = CommonArticles.objects.filter(schvaleno='a', rubrika=creative_page_slug).order_by('-datum')[:5]


    return render(request, 'common-articles/list.html', {
        'heading': COMMON_ARTICLES_CREATIVE_PAGES[creative_page_slug]['name'],
        'articles': articles,
        'creative_page_slug': creative_page_slug,
        'creative_page_slug_en': en_slug,
    })


def common_article_detail(request, creative_page_slug, article_id, article_slug):

    try:
        en_slug = SLUG_NAME_TRANSLATION_FROM_CZ[creative_page_slug]
    except KeyError:
        raise Http404()

    article = get_object_or_404(CommonArticles, id=article_id)
    if article.get_slug() != article_slug:
        raise NotImplementedError()
        # TODO: reverse url search in view
        # raise HttpResponseRedirect()


    return render(request, 'common-articles/detail.html', {
        'heading': COMMON_ARTICLES_CREATIVE_PAGES[creative_page_slug]['name'],
        'article': article,
        'creative_page_slug': creative_page_slug,
        'creative_page_slug_en': en_slug,
    })

def change_skin(request):
    new_skin = request.GET.get('skin', 'light')
    if new_skin not in VALID_SKINS:
        return HttpResponseBadRequest("Nerozpoznán skin, který bych mohl nastavit.")

    request.session['skin'] = new_skin

    return HttpResponseRedirect("/")
