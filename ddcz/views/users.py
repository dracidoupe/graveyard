import logging

from django.urls.base import reverse
from ddcz.models.used.users import UzivateleCekajici
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.paginator import Paginator
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import resolve, Resolver404
from django.views.decorators.http import require_POST, require_http_methods

from ..text import misencode
from ..models import (
    Author,
    UserProfile,
    UzivateleCekajici,
    LEVEL_DESCRIPTIONS,
)

DRAGON_EGG_POST_NAME = "dragon_egg"
DRAGON_EGG_BIRTH_CONFIRMER_LEVEL = ["6", "8"]
DEFAULT_USER_LIST_SIZE = 50
VALID_SKINS = ["light", "dark", "historic"]

logger = logging.getLogger(__name__)


@require_http_methods(["HEAD", "GET"])
def users_list(request):
    # TODO: Displaying newbies & mentats
    # Original query:
    #    $vysledek = MySQL_Query("SELECT a.id, a.nick_uzivatele, a.email_uzivatele, a.vypsat_udaje, a.level $co_vypsat, b.locked as mentat_id, c.newbie_id
    #             FROM uzivatele a left outer join mentat_newbie b
    #                ON (a.id = b.mentat_id) and (b.newbie_id = 0)
    #                left outer join mentat_newbie c
    #                ON (a.id = c.newbie_id) and (c.mentat_id = 0) and (c.locked='0')
    #                ".
    #                $podminka."
    #             ORDER BY ".AddSlashes($ord)." ".AddSlashes($j_ord)." ".addslashes($limit));
    # users = (
    #     UserProfile.objects.filter(  # .all()
    #         Q(newbies__locked="0", newbies__mentat_id=0)
    #         | Q(mentats__locked="1", mentats__newbie_id=0)
    #     )  # .annotate(id_count=Count("id"))
    #     .order_by("-pospristup")
    # )
    # print(str(users.query))
    searched_nick = request.GET.get("nick", None)
    search_limited = False

    if searched_nick:
        if len(searched_nick) <= 3:
            users = UserProfile.objects.filter(nick=misencode(searched_nick)).order_by(
                "nick"
            )
            search_limited = True
        else:
            users = UserProfile.objects.filter(
                nick__icontains=misencode(searched_nick)
            ).order_by("nick")
    else:
        users = UserProfile.objects.all().order_by("-last_login")

    paginator = Paginator(users, DEFAULT_USER_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    users = paginator.get_page(page)

    return render(
        request,
        "users/list.html",
        {
            "users": users,
            "searched_nick": searched_nick or "",
            "search_limited": search_limited,
        },
    )


@require_http_methods(["HEAD", "GET"])
def user_profile(request, user_profile_id, nick_slug):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    try:
        creations = Author.objects.get(user=user_profile).get_all_creations()
    except Author.DoesNotExist as e:
        creations = False

    description = LEVEL_DESCRIPTIONS["0"]
    if user_profile.level in LEVEL_DESCRIPTIONS:
        description = LEVEL_DESCRIPTIONS[user_profile.level]

    level_stars = {
        level: staticfiles_storage.url(
            f"skins/{request.session.get('skin', 'light')}/img/star-level-{ level }.svg"
        )
        for level in LEVEL_DESCRIPTIONS
    }

    return render(
        request,
        "users/detail.html",
        {
            "profile": user_profile,
            "permission": user_profile.public_listing_permissions,
            "creations": creations,
            "level_stars": level_stars,
            "level_description": description,
        },
    )


@require_http_methods(["HEAD", "GET"])
def change_skin(request):
    new_skin = request.GET.get("skin", "light")
    if new_skin not in VALID_SKINS:
        return HttpResponseBadRequest("Nerozpoznán skin, který bych mohl nastavit.")
    request.session["skin"] = new_skin

    try:
        redirect_url = request.GET.get("redirect", "/")
        resolve(redirect_url)
    except Resolver404:
        redirect_url = "/"

    return HttpResponseRedirect(redirect_url)


@require_http_methods(["HEAD", "GET", "POST"])
def awaiting(request):
    registrations = UzivateleCekajici.objects.all().order_by("-date")
    isAwaiting = registrations.count() is not 0

    if request.method == "POST":
        if request.POST.get("f") == "patronize":
            try:
                profile_id = request.user.userprofile.id
                registration = UzivateleCekajici.objects.get(
                    id=request.POST.get(DRAGON_EGG_POST_NAME)
                )
                registration.patronize(profile_id)
            except UzivateleCekajici.DoesNotExist:
                logger.error(
                    f"User with primary key ID {profile_id} wanted to get a newbie, but no such user exists."
                )
            except:
                pass  # log if user does not exists or not having permissions
            return HttpResponseRedirect(reverse("ddcz:awaiting-registrations"))

    return render(
        request,
        "users/awaiting-registrations.html",
        {
            "registrations": registrations,
            "awaiting": isAwaiting,
            "dragon_keeper": DRAGON_EGG_POST_NAME,
            "dragon_confirming_levels": DRAGON_EGG_BIRTH_CONFIRMER_LEVEL,
        },
    )
