import logging

from django.apps import apps
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

from ddcz.models import CreativePage, UserProfile


logger = logging.getLogger(__name__)

# In the constant below: It is possible to vary the redirections.
# It is preferable to do so via the constants rather than changing
# the code if there is no real need for it, so the legacy router
# remains automatized.

CREATION_LIST = ["prispevky", "prispevky_komp"]
CREATION_DETAIL = "prispevky_precti"
USER_DETAIL = ["uzivatele_podrobnosti", "runy_ciziod", "runy_cizipro"]

# Forbidden dictionary keys for PAGE_TO_VIEW_MAP:
#  - Anything from CREATION and CREATION_DETAIL
#  - Anything from ALLOWED_CREATION_PAGES
PAGE_TO_VIEW_MAP = {
    "aktuality": "ddcz:news",
    "novinky": "ddcz:newsfeed",
    "uzivatele": "ddcz:users-list",
    "registrace": "ddcz:sign-up",
    "seznamka": "ddcz:dating",
    "forum": "ddcz:phorum-list",
    "linky": "ddcz:links-list",
    "inzerce": "ddcz:market",
    "credits": "ddcz:web-authors-and-editors",
    "faq": "ddcz:website-manual",
    "oao": "ddcz:faq",
    "cojetodrd": "ddcz:about-drd",
    "posta": "ddcz:postal-service",
}

COMMON_ARTICLES_NAME_MAP = {
    "hrbitov": "hrbitov",
    "clanky": "clanky",
    "expanze": "expanze",
    "kouzelnikzvl": "kouzelnikzvl",
    "alchymistazvl": "alchymistazvl",
    "valecnik": "valecnik",
    "hranicar": "hranicar",
    "zlodej": "zlodej",
    "novapovolani": "novapovolani",
    "noverasy": "noverasy",
}

PRINT_CATEGORIES_TO_CREATIVE_PAGE_MAP = {
    "dovednosti": "dovednosti",
    "hranicarkouzla": "hranicar",
}


ALLOWED_CREATION_PAGES = [
    "bestiar",
    "dobrodruzstvi",
    "predmety",
    "kouzla",
    "alchpredmety",
    "hranicarkouzla",
    "dovednosti",
    "galerie",
    "fotogalerie",
]


@require_http_methods(["HEAD", "GET"])
def legacy_router(request):
    page_category = request.GET.get("rub", False)
    page_creation_type = request.GET.get("co", False)
    id = request.GET.get("id", False)

    # The LEGACY_PLAIN_ROUTER is redirecting basic pages.
    # Typically no creative pages are present here.
    if page_category in PAGE_TO_VIEW_MAP.keys():
        return HttpResponseRedirect(reverse(PAGE_TO_VIEW_MAP[page_category]))

    # Some of the creation have legacy url
    # index.php?rub=prispevky(_komp)&co=page_slug
    # Here are lists of such creative pages.
    if (
        page_category in CREATION_LIST
        and page_creation_type in COMMON_ARTICLES_NAME_MAP.keys()
    ):
        return HttpResponseRedirect(
            reverse(
                "ddcz:creation-list",
                kwargs={
                    "creative_page_slug": COMMON_ARTICLES_NAME_MAP[page_creation_type]
                },
            )
        )

    # For index.php?rub=prispevky_jeden&subsection=page_slug&id=article_id
    # we can find the article detail by Id.
    if page_category == CREATION_DETAIL and id is not False:
        page = get_object_or_404(CreativePage, slug=page_creation_type)
        return get_creation_detail_redirect(page, id)

    # For index.php?rub=uzivatele_podrobnosti&skin=light&id=13591
    # Also for runes, just redirect here
    if page_category in USER_DETAIL and id is not False:
        user_profile = get_object_or_404(UserProfile)
        return HttpResponsePermanentRedirect(
            reverse(
                "ddcz:user-detail",
                kwargs={
                    "user_profile_id": user_profile.id,
                    "nick_slug": user_profile.slug,
                },
            )
        )

    # There are some special creative pages that are not stored
    # as the others, those have their own tables in the database.
    # For those we have lists and details in this for loop.
    for name in ALLOWED_CREATION_PAGES:
        if page_category in [name, name + "_komp"]:
            return HttpResponseRedirect(
                reverse(
                    "ddcz:creation-list",
                    kwargs={"creative_page_slug": name},
                )
            )
        if page_category in [name + "_jeden"]:
            page = get_object_or_404(CreativePage, slug=name)
            return get_creation_detail_redirect(page, id)

    ###  Finally if no route is found, redirect to news and log
    logger.warning(
        f"There has been submitted URL address from the old website: index.php >> No redirect could be found for a legacy URL {request.get_full_path()}"
    )
    return HttpResponseRedirect(reverse("ddcz:news"))


def get_creation_detail_redirect(page, article_id):
    app, class_name = page.model_class.split(".")
    model = apps.get_model(app, class_name)
    article = get_object_or_404(model, id=article_id)
    return HttpResponsePermanentRedirect(
        reverse(
            "ddcz:creation-detail",
            kwargs={
                "creative_page_slug": page.slug,
                "creation_id": article_id,
                "creation_slug": article.get_slug(),
            },
        )
    )


@require_http_methods(["HEAD", "GET"])
def print_legacy_router(request, page_category, page_category_second):
    id = request.GET.get("id", False)

    if page_category in ALLOWED_CREATION_PAGES:
        page = CreativePage.objects.get(slug=page_category)
        return get_creation_detail_redirect(page, id)

    ###  Finally if no route is found, redirect to news and log
    logger.warning(
        f"Bad print redirect: No redirect could be found for a legacy URL {request.get_full_path()}"
    )
    return HttpResponseRedirect(reverse("ddcz:news"))
