import logging
from urllib.parse import urljoin
from zlib import crc32

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import (
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseNotAllowed,
    Http404,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..creations import ApprovalChoices
from ..forms.comments import CreationCommentForm, CommentAction
from ..html import check_creation_html, HtmlTagMismatchException
from ..models import (
    Author,
    CreativePage,
    CreativePageConcept,
    CreationComment,
    DownloadItem,
    Quest,
)
from ..text import escape_user_input

# Get an instance of a logger
logger = logging.getLogger(__name__)

VALID_SKINS = ["light", "dark", "historic"]
DEFAULT_LIST_SIZE = 25
DEFAULT_GALLERY_LIST_SIZE = 16
DEFAULT_USER_LIST_SIZE = 50

MAP_CREATION_TEMPLATE = {
    "downloaditem": "downloaditem-list.html",
    "quest": "quest-list.html",
    "photo": "photo-list.html",
    "gallerypicture": "gallerypicture-list.html",
    "default": "creations-list.html",
}


@require_http_methods(["HEAD", "GET"])
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
        # For Common Articles, Creative Page is stored in attribute 'creative_page_slug' as slug
        # For everything else, Creative Page is determined by its model class
        if model_class_name == "commonarticle":
            article_list = model_class.objects.filter(
                is_published=ApprovalChoices.APPROVED.value,
                creative_page_slug=creative_page_slug,
            ).order_by("-published")
        else:
            article_list = model_class.objects.filter(
                is_published=ApprovalChoices.APPROVED.value
            ).order_by("-published")

        if creative_page_slug in ["galerie", "fotogalerie"]:
            default_limit = DEFAULT_GALLERY_LIST_SIZE
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

    try:
        template = MAP_CREATION_TEMPLATE[model_class_name]
    except KeyError:
        template = MAP_CREATION_TEMPLATE["default"]

    return render(
        request,
        "creative-pages/" + template,
        {
            "heading": creative_page.name,
            "articles": articles,
            "creative_page_slug": creative_page.slug,
            "concept": concept,
        },
    )


def get_creation_info(creative_page_slug, creation_id, creation_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split(".")
    model_class = apps.get_model(app, model_class_name)

    cache_key = f"creation:{model_class_name}:article:{int(creation_id)}:{crc32(creation_slug.encode('utf8'))}"

    article = cache.get(cache_key)

    if not article:
        if model_class_name == "commonarticle":
            article = get_object_or_404(
                model_class,
                id=creation_id,
                is_published=ApprovalChoices.APPROVED.value,
                creative_page_slug=creative_page_slug,
            )
        else:
            article = get_object_or_404(
                model_class, is_published=ApprovalChoices.APPROVED.value, id=creation_id
            )

        if article.get_slug() != creation_slug:
            e = ValueError()
            e.url = reverse(
                "ddcz:creation-detail",
                kwargs={
                    "creative_page_slug": creative_page_slug,
                    "creation_id": article.pk,
                    "creation_slug": article.get_slug(),
                },
            )
            raise e
        else:
            cache.set(cache_key, article)

    return {
        "article": article,
        "model_class": model_class,
        "model_class_name": model_class_name,
        "creative_page": creative_page,
    }


@require_http_methods(["HEAD", "GET", "POST"])
def creation_detail(request, creative_page_slug, creation_id, creation_slug):
    try:
        creation_info = get_creation_info(
            creative_page_slug, creation_id, creation_slug
        )
    except ValueError as e:
        return HttpResponsePermanentRedirect(e.url)

    if request.method == "POST" and request.POST["post_type"] and request.user:
        # TODO: Comment deletion
        # if (
        #     request.POST["post_type"] == DELETE_PHORUM_COMMENT
        #     and request.POST["submit"] == "Smazat"
        # ):
        #     try:
        #         Phorum.objects.get(
        #             id=request.POST["post_id"],
        #             nickname=request.user.profile.nick,
        #         ).delete()
        #     except Phorum.DoesNotExist as e:
        #         messages.error(request, "Zprávu se nepodařilo smazat.")
        #         return HttpResponseRedirect(reverse("ddcz:phorum-list"))

        if (
            request.POST["post_type"] == CommentAction.ADD.value
            and request.POST["submit"] == "Přidej"
        ):
            creation_comment_form = CreationCommentForm(request.POST)
            if creation_comment_form.is_valid():
                # TODO DISPATCH: Here we need to dispatch e-mails etc.
                CreationComment.objects.create(
                    reputation=0,
                    user=request.user.profile,
                    text=escape_user_input(creation_comment_form.cleaned_data["text"]),
                    nickname=request.user.profile.nick,
                    email=request.user.profile.email,
                    foreign_id=creation_info["article"].pk,
                    # Yes this looks weird, but see docs for CreationComment model
                    foreign_table=creative_page_slug,
                )
                return HttpResponseRedirect(
                    reverse(
                        "ddcz:creation-detail",
                        kwargs={
                            "creative_page_slug": creative_page_slug,
                            "creation_id": creation_info["article"].pk,
                            "creation_slug": creation_info["article"].get_slug(),
                        },
                    )
                )
    else:
        creation_comment_form = CreationCommentForm()

    return render(
        request,
        f"creative-pages/{creation_info['model_class_name']}-detail.html",
        {
            "heading": creation_info["creative_page"].name,
            "article": creation_info["article"],
            "creative_page_slug": creative_page_slug,
            "comment_page": request.GET.get("z_s", 1),
            "creation_comment_form": CreationCommentForm(),
        },
    )


@require_http_methods(["HEAD", "GET"])
def creation_detail_image(
    # TODO: Deduplicate
    request,
    creative_page_slug,
    creation_id,
    creation_slug,
    image_path,
):
    try:
        get_creation_info(creative_page_slug, creation_id, creation_slug)
    except ValueError as e:
        return HttpResponsePermanentRedirect(e.url)

    return HttpResponsePermanentRedirect(
        f"{settings.CREATION_PICTURES_MEDIA_ROOT_URL}{image_path}"
    )


# This allows unfiltered traversion of the static path; shouldn't be a problem in the s3 bucket,
# but should be deleted if we're moving somewhere else
@require_http_methods(["HEAD", "GET"])
def creation_detail_image_legacy(
    request,
    image_path,
):
    return HttpResponsePermanentRedirect(
        f"{settings.CREATION_PICTURES_MEDIA_ROOT_URL}{image_path}"
    )


@require_http_methods(["HEAD", "GET"])
def creative_page_concept(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    try:
        concept = creative_page.creativepageconcept
    except CreativePageConcept.DoesNotExist:
        raise Http404()

    return render(
        request,
        "creative-pages/concept.html",
        {
            "heading": creative_page.name,
            "creative_page_slug": creative_page_slug,
            "concept": concept,
        },
    )


@require_http_methods(["HEAD", "GET", "POST"])
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

        # For Common Articles, Creative Page is stored in attribute 'creative_page_slug' as slug
        # For everything else, Creative Page is determined by its model class
        if model_class_name == "commonarticle":
            creations_list = model_class.objects.filter(
                is_published=ApprovalChoices.APPROVED.value,
                creative_page_slug=creative_page_slug,
            ).order_by("-published")
        else:
            creations_list = model_class.objects.filter(
                is_published=ApprovalChoices.APPROVED.value
            ).order_by("-published")

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


@require_http_methods(["HEAD", "GET"])
def download_file(request, download_id):
    download_item = get_object_or_404(DownloadItem, pk=download_id)
    download_item.download_counter += 1
    download_item.save()
    return HttpResponseRedirect(download_item.item.url)


@require_http_methods(["HEAD", "GET"])
def quest_view_redirect(request, quest_id, quest_slug=None):
    quest = get_object_or_404(Quest, pk=quest_id)
    if quest_slug is None:
        return HttpResponsePermanentRedirect(
            reverse(
                "ddcz:quest-view",
                kwargs={"quest_id": quest_id, "quest_slug": quest.get_slug()},
            )
        )

    quest.read += 1
    quest.save()
    return HttpResponseRedirect(quest.get_final_url())


# For content like /dobrodruzstvi/13/img/kylmar.gif
@require_http_methods(["HEAD", "GET"])
def quest_view_redirect_rest(request, quest_id, quest_slug=None, leftover=None):
    quest = get_object_or_404(Quest, pk=quest_id)
    return HttpResponseRedirect(urljoin(quest.get_final_url(), leftover))


@require_http_methods(["HEAD", "GET"])
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
