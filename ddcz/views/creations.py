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
from django.db.models.expressions import OuterRef, Subquery
from django.http import (
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
    Http404,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy, resolve, Resolver404
from django.contrib.auth import (
    authenticate,
    login as login_auth,
    views as authviews,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..commonarticles import (
    SLUG_NAME_TRANSLATION_FROM_CZ,
    COMMON_ARTICLES_CREATIVE_PAGES,
)

from ..html import check_creation_html, HtmlTagMismatchException
from ..models import (
    MARKET_SECTION_CHOICES,
    Author,
    CreativePage,
    CreativePageConcept,
    DownloadItem,
    Quest,
    LEVEL_DESCRIPTIONS,
)


# Get an instance of a logger
logger = logging.getLogger(__name__)

VALID_SKINS = ["light", "dark", "historic"]
DEFAULT_LIST_SIZE = 10
DEFAULT_USER_LIST_SIZE = 50


@require_http_methods(["GET"])
@vary_on_cookie
def creative_page_list(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split(".")
    model_class = apps.get_model(app, model_class_name)
    page = request.GET.get("z_s", 1)
    articles = None

    cache_key = f"creative-page:{creative_page.slug}:list"
    if page == 1:
        articles = cache.get(cache_key)

    if not articles:
        # For Common Articles, Creative Page is stored in attribute 'rubrika' as slug
        # For everything else, Creative Page is determined by its model class
        if model_class_name == "commonarticle":
            article_list = model_class.objects.filter(
                schvaleno="a", rubrika=creative_page_slug
            ).order_by("-datum")
        else:
            article_list = model_class.objects.filter(schvaleno="a").order_by("-datum")

        if creative_page_slug in ["galerie", "fotogalerie"]:
            default_limit = 18
        else:
            default_limit = DEFAULT_LIST_SIZE

        paginator = Paginator(article_list, default_limit)

        articles = paginator.get_page(page)

        if page == 1:
            cache.set(cache_key, articles)

    try:
        concept = creative_page.creativepageconcept
    except CreativePageConcept.DoesNotExist:
        concept = None

    return render(
        request,
        "creative-pages/%s-list.html" % model_class_name,
        {
            "heading": creative_page.name,
            "articles": articles,
            "creative_page_slug": creative_page.slug,
            "concept": concept,
        },
    )


@require_http_methods(["GET"])
def creation_detail(request, creative_page_slug, creation_id, creation_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split(".")
    model_class = apps.get_model(app, model_class_name)

    cache_key = f"creation:{model_class_name}:article:{int(creation_id)}:{crc32(creation_slug.encode('utf8'))}"

    article = cache.get(cache_key)

    if not article:
        article = get_object_or_404(model_class, id=creation_id)
        if article.get_slug() != creation_slug:
            return HttpResponsePermanentRedirect(
                reverse(
                    "ddcz:creation-detail",
                    kwargs={
                        "creative_page_slug": creative_page_slug,
                        "creation_id": article.pk,
                        "creation_slug": article.get_slug(),
                    },
                )
            )
        else:
            cache.set(cache_key, article)

    return render(
        request,
        "creative-pages/%s-detail.html" % model_class_name,
        {
            "heading": creative_page.name,
            "article": article,
            "creative_page_slug": creative_page_slug,
            "comment_page": request.GET.get("z_s", 1),
        },
    )


@require_http_methods(["GET"])
def creative_page_concept(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    try:
        concept = creative_page.creativepageconcept
    except CreativePageConcept.DoesNotExist:
        raise Http404

    return render(
        request,
        "creative-pages/concept.html",
        {
            "heading": creative_page.name,
            "creative_page_slug": creative_page_slug,
            "concept": concept,
        },
    )


@require_http_methods(["GET", "POST"])
def creative_page_html_check(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)

    if request.method == "GET":
        return render(
            request,
            "creative-pages/html-check-form.html",
            {
                "heading": creative_page.name,
            },
        )

    if request.method == "POST":
        app, model_class_name = creative_page.model_class.split(".")
        model_class = apps.get_model(app, model_class_name)

        # For Common Articles, Creative Page is stored in attribute 'rubrika' as slug
        # For everything else, Creative Page is determined by its model class
        if model_class_name == "commonarticle":
            creations_list = model_class.objects.filter(
                schvaleno="a", rubrika=creative_page_slug
            ).order_by("-datum")
        else:
            creations_list = model_class.objects.filter(schvaleno="a").order_by(
                "-datum"
            )

        bad_creations = []

        for creation in creations_list:
            for attr in model_class.legacy_html_attributes:
                try:
                    check_creation_html(getattr(creation, attr))
                except HtmlTagMismatchException as err:
                    message = f"V položce {attr} je tato chyba: {str(err)}"
                    bad_creations.append({"creation": creation, "message": message})

        return render(
            request,
            "creative-pages/html-check-list.html",
            {
                "heading": creative_page.name,
                "creative_page_slug": creative_page_slug,
                "bad_creations": bad_creations,
            },
        )

    return HttpResponseNotAllowed(["GET", "POST"])


@require_http_methods(["GET"])
def download_file(request, download_id):
    download_item = get_object_or_404(DownloadItem, pk=download_id)
    download_item.download_counter += 1
    download_item.save()
    return HttpResponseRedirect(download_item.item.url)


@require_http_methods(["GET"])
def quest_view_redirect(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    quest.precteno += 1
    quest.save()
    return HttpResponseRedirect(quest.get_final_url())


@require_http_methods(["GET"])
def author_detail(request, author_id, slug):
    author = get_object_or_404(Author, id=author_id)

    if author.slug != slug:
        return HttpResponsePermanentRedirect(
            reverse(
                "ddcz:author-detail",
                kwargs={
                    "author_id": author.pk,
                    "slug": author.slug,
                },
            )
        )

    return render(
        request,
        "creations/author-detail.html",
        {
            "author": author,
            "pages_with_creations": author.get_all_creations(),
        },
    )
