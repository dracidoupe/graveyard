import logging
from django.apps import apps
from ddcz.models.used.creations import Creation, CreativePage
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

# In the constant below: It is possible to vary the redirections.
# It is preferable to do so via the constants rather than changing
# the code if there is no real need for it, so the legacy router
# remains automatized.

CREATION = ["prispevky", "prispevky_komp"]
CREATION_DETAIL = "prispevky_precti"

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


@require_http_methods(["GET"])
def legacy_router(request):

    section = request.GET.get("rub", False)
    subsection = request.GET.get("co", False)
    id = request.GET.get("id", False)

    # The LEGACY_PLAIN_ROUTER is redirecting basic pages.
    # Typically no creative pages are present here.
    if section in PAGE_TO_VIEW_MAP.keys():
        return HttpResponseRedirect(reverse(PAGE_TO_VIEW_MAP[section]))

    # Some of the creation have legacy url
    # index.php?rub=prispevky(_komp)&co=page_slug
    # Here are lists of such creative pages.
    if section in CREATION and subsection in COMMON_ARTICLES_NAME_MAP.keys():
        return HttpResponseRedirect(
            reverse(
                "ddcz:creation-list",
                kwargs={"creative_page_slug": COMMON_ARTICLES_NAME_MAP[subsection]},
            )
        )

    # For index.php?rub=prispevky_jeden&subsection=page_slug&id=article_id
    # we can find the article detail by Id.
    if section == CREATION_DETAIL and id is not False:
        page = get_object_or_404(CreativePage, slug=subsection)
        return get_creation_detail_redirect(page, id)

    # There are some special creative pages that are not stored
    # as the others, those have their own tables in the database.
    # For those we have lists and details in this for loop.
    for name in ALLOWED_CREATION_PAGES:
        if section in [name, name + "_komp"]:
            return HttpResponseRedirect(
                reverse(
                    "ddcz:creation-list",
                    kwargs={"creative_page_slug": name},
                )
            )
        if section in [name + "_jeden"]:
            page = get_object_or_404(CreativePage, slug=name)
            return get_creation_detail_redirect(page, id)

    ###  Finally if no route is found, redirect to news
    logger = logging.getLogger(__name__)
    logger.info(
        "There has been submitted URL address from the old website: index.php | rub: "
        + section
        + ", co: "
        + subsection
        + ", id: "
        + id
        + "."
    )
    return HttpResponseRedirect(reverse("ddcz:news"))


def get_creation_detail_redirect(page, article_id):
    app, class_name = page.model_class.split(".")
    model = apps.get_model(app, class_name)
    article = get_object_or_404(model, id=article_id)
    return HttpResponseRedirect(
        reverse(
            "ddcz:creation-detail",
            kwargs={
                "creative_page_slug": page.slug,
                "creation_id": article_id,
                "creation_slug": article.get_slug(),
            },
        )
    )
