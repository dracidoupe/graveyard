from ddcz.models.used.creations import CreativePage
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

CREATION = ["prispevky", "prispevky_komp"]
CREATION_DETAIL = "prispevky_precti"

# Forbidden dictionary keys from CREATION and CREATION_DETAIL
LEGACY_PLAIN_ROUTER = {
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

LEGACY_BASIC_CREATION_ROUTER = {
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

LEGACY_CREATION_ROUTER = [
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

    get = dict(request.GET)
    section = handle_get_key(get, "rub")
    subsection = handle_get_key(get, "co")
    id = handle_get_key(get, "id")

    ### Basic pages and lists
    if section in LEGACY_PLAIN_ROUTER.keys():
        return HttpResponseRedirect(reverse(LEGACY_PLAIN_ROUTER[section]))

    if section in CREATION and subsection in LEGACY_BASIC_CREATION_ROUTER.keys():
        return HttpResponseRedirect(
            "/rubriky/" + LEGACY_BASIC_CREATION_ROUTER[subsection]
        )

    for name in LEGACY_CREATION_ROUTER:
        if section in [name, name + "_komp"]:
            return HttpResponseRedirect("/rubriky/" + name)

    ### The specific creation
    if section == CREATION_DETAIL and id is not False:
        pass

    ###  Finally if no route is found, redirect to news feed
    return HttpResponse(reverse("ddcz:news"))


def handle_get_key(get, key):
    try:
        return get[key][0]
    except KeyError:
        return False
