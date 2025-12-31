from hashlib import md5
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as login_auth,
    views as authviews,
)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import (
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from ..forms.authentication import LoginForm, PasswordResetForm
from ..forms.signup import SignUpForm
from ..users import migrate_user, logout_user_without_losing_session

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def logout(request):
    referer = request.META.get("HTTP_REFERER", "/")

    logout_user_without_losing_session(request)
    return HttpResponseRedirect(referer)


@require_http_methods(["POST"])
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

    referer = request.META.get("HTTP_REFERER", "/")

    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.error(request, f"Špatně vyplněný formulář: {form.errors.as_text()}")
        return HttpResponseRedirect(referer)

    from ddcz.models import UserProfile

    user = authenticate(
        username=form.cleaned_data["nick"], password=form.cleaned_data["password"]
    )

    if user is not None:
        # Deny login to banned users (legacy: status == '1')
        if hasattr(user, "profile") and user.profile.status == "1":
            messages.error(
                request, "Váš účet je zablokován. Kontaktujte prosím redakci."
            )
            return HttpResponseRedirect(referer)
        login_auth(request, user)
        user.profile.last_login = timezone.now()
        user.profile.save()
        return HttpResponseRedirect(referer)
    else:
        m = md5()
        # TODO: Encoding needs verification
        # This needs to be done since passwords, of course, can contain
        # non-ascii characters that affect hashing
        m.update(form.cleaned_data["password"].encode("cp1250"))
        old_insecure_hashed_password = m.hexdigest()

        try:
            profile = UserProfile.objects.get(nick=form.cleaned_data["nick"])
        except UserProfile.DoesNotExist:
            messages.error(request, "Špatný nick a nebo heslo")
            return HttpResponseRedirect(referer)

        # Deny login to banned users even if they match legacy password
        if profile.status == "1":
            messages.error(
                request, "Váš účet je zablokován. Kontaktujte prosím redakci."
            )
            return HttpResponseRedirect(referer)

        if profile.password_v1 != old_insecure_hashed_password:
            messages.error(request, "Špatný nick a nebo heslo")
            return HttpResponseRedirect(referer)

        else:
            migrate_user(profile=profile, password=form.cleaned_data["password"])
            user = authenticate(
                username=form.cleaned_data["nick"],
                password=form.cleaned_data["password"],
            )

            if not user:
                logger.error(
                    f"Error when migrating user {form.cleaned_data['nick']} to User table, see logs"
                )
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


def sign_up(request):
    form = SignUpForm()

    if request.method == "POST" and request.POST.get("submit"):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                "users/sign_up_after.html",
                {"addressing": form.cleaned_data["salutation"]},
            )

    return render(
        request,
        "users/sign_up.html",
        {
            "sign_up_form": form,
            "reg_script": staticfiles_storage.url("common/js/main.js"),
            "reg_style": staticfiles_storage.url("common/css/registration.css"),
            "seal_image": staticfiles_storage.url(
                "common/img/registration-seal-gold.svg"
            ),
        },
    )
