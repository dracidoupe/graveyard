from hashlib import md5
import logging
from smtplib import SMTPException

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseBadRequest,
    HttpResponseServerError,
    Http404,
)
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy, resolve, Resolver404

from django.contrib.auth import (
    authenticate,
    login as login_auth,
    logout as logout_auth,
    views as authviews,
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages

from .commonarticles import (
    SLUG_NAME_TRANSLATION_FROM_CZ,
    COMMON_ARTICLES_CREATIVE_PAGES,
)
from .forms.authentication import LoginForm, PasswordResetForm
from .forms.comments import PhorumCommentForm, DeletePhorumCommentForm
from .models import (
    Author,
    CommonArticle,
    CreativePage,
    CreativePageConcept,
    DownloadItem,
    Dating,
    Link,
    News,
    Quest,
    Phorum,
    UserProfile,
)
from .users import migrate_user

# Get an instance of a logger
logger = logging.getLogger(__name__)

VALID_SKINS = ["light", "dark"]
DEFAULT_LIST_SIZE = 5


def index(request):
    news_list = News.objects.order_by("-datum")

    paginator = Paginator(news_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    news = paginator.get_page(page)

    return render(request, "news/list.html", {"news": news})


def creative_page_list(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split(".")
    model_class = apps.get_model(app, model_class_name)

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
    page = request.GET.get("z_s", 1)

    articles = paginator.get_page(page)

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


def creation_detail(request, creative_page_slug, creation_id, creation_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split(".")
    model_class = apps.get_model(app, model_class_name)

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

    return render(
        request,
        "creative-pages/%s-detail.html" % model_class_name,
        {
            "heading": creative_page.name,
            "article": article,
            "creative_page_slug": creative_page_slug,
        },
    )


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


def download_file(request, download_id):
    download_item = get_object_or_404(DownloadItem, pk=download_id)
    download_item.download_counter += 1
    download_item.save()
    return HttpResponseRedirect(download_item.item.url)


def quest_view_redirect(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    quest.precteno += 1
    quest.save()
    return HttpResponseRedirect(quest.get_final_url())


def links(request):
    item_list = Link.objects.filter(schvaleno="a").order_by("-datum")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "links/list.html", {"items": items})


def dating(request):
    item_list = Dating.objects.order_by("-datum")

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get("z_s", 1)

    items = paginator.get_page(page)

    return render(request, "dating/list.html", {"items": items})


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


def logout(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Use POST.")

    referer = request.META.get("HTTP_REFERER", "/")

    logout_auth(request)
    return HttpResponseRedirect(referer)


def login(request):
    """
    Log user in from one of the two sources:

        * Normal Django's authentication framework
        * Legacy DDCZ database

    If user is able to log in from legacy database table and does not have
    corresponding user object, create it for him.

    After this version of the site will become the default one, also delete User's
    password from the legacy table and consider them "migrated".

    Note that it is unusal for this form to handle only POST data and creates
    a bit of a weird experience with the form--but given the form is present
    on each and every page, it feels better to do this than to feed this kind
    of POST handling to every view.
    """

    if request.method != "POST":
        return HttpResponseBadRequest("Use POST.")

    referer = request.META.get("HTTP_REFERER", "/")

    form = LoginForm(request.POST)

    if not form.is_valid():
        return HttpResponseRedirect(referer)

    user = authenticate(
        username=form.cleaned_data["nick"], password=form.cleaned_data["password"]
    )
    if user is not None:
        login_auth(request, user)
        return HttpResponseRedirect(referer)
    else:
        m = md5()
        # TODO: Encoding needs verification
        # This needs to be done since passwords, of course, can contain
        # non-ascii characters that affect hashing
        m.update(form.cleaned_data["password"].encode("cp1250"))
        old_insecure_hashed_password = m.hexdigest()

        try:
            profile = UserProfile.objects.get(nick_uzivatele=form.cleaned_data["nick"])
        except UserProfile.DoesNotExist:
            messages.error(request, "Špatný nick a nebo heslo")
            return HttpResponseRedirect(referer)

        if profile.psw_uzivatele != old_insecure_hashed_password:
            messages.error(request, "Špatný nick a nebo heslo")
            return HttpResponseRedirect(referer)

        else:
            migrate_user(profile=profile, password=form.cleaned_data["password"])
            user = authenticate(
                username=form.cleaned_data["nick"],
                password=form.cleaned_data["password"],
            )

            if not user:
                return HttpResponseServerError(
                    "Chyba během migrace na nový systém! Prosím kontaktujte Almada"
                )

            login_auth(request, user)

            # TODO: For first-time login, bunch of stuff happens. Inspect legacy login and reimplement

            return HttpResponseRedirect(referer)


class PasswordResetView(authviews.PasswordResetView):
    template_name = "users/password-reset.html"
    success_url = reverse_lazy("ddcz:password-reset-done")
    from_email = settings.DDCZ_TRANSACTION_EMAIL_FROM
    email_template_name = "users/password-reset-email.html"
    form_class = PasswordResetForm


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class PasswordResetConfirmView(authviews.PasswordResetConfirmView):
    template_name = "users/password-change.html"
    success_url = reverse_lazy("ddcz:password-change-done")


class PasswordResetCompleteView(authviews.PasswordResetCompleteView):
    template_name = "users/password-change-done.html"


def user_profile(request, user_profile_id, nick_slug):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)

    return render(
        request,
        "users/detail.html",
        {
            "profile": user_profile,
        },
    )


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


def phorum(request):
    if request.method == "POST" and request.POST["post_type"] and request.user:
        if request.POST["post_type"] == "d" and request.POST["submit"] == "Smazat":
            try:
                Phorum.objects.get(
                    id=request.POST["post_id"],
                    nickname=request.user.profile.nick_uzivatele,
                ).delete()
            except Phorum.DoesNotExist as e:
                messages.error(request, "Zprávu se nepodařilo smazat.")
                return HttpResponseRedirect(reverse("ddcz:phorum-list"))

        elif request.POST["post_type"] == "a" and request.POST["submit"] == "Přidej":
            form = PhorumCommentForm(request.POST)
            if form.is_valid():
                Phorum.objects.create(
                    reputace=0,
                    reg=1,
                    user=request.user.profile,
                    text=form.cleaned_data["text"],
                    nickname=request.user.profile.nick_uzivatele,
                    email=request.user.profile.email_uzivatele,
                )

        return HttpResponseRedirect(reverse("ddcz:phorum-list"))

    default_limit = 20
    discussions = Phorum.objects.all().order_by("-datum")

    paginator = Paginator(discussions, default_limit)
    page = request.GET.get("z_s", 1)

    discussions = paginator.get_page(page)

    return render(
        request,
        "discussions/phorum-list.html",
        {
            "discussions": discussions,
            "phorum_comment_form": PhorumCommentForm(),
            "delete_form": DeletePhorumCommentForm(),
        },
    )
