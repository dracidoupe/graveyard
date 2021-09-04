from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.views import decorators
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from ddcz.models import LevelSystemParams, UserProfile, AwaitingRegistration

from .forms.dashboard import FormTypes
from .forms.users import RegistrationRequestApproval


@decorators.staff_member_required()
def dashboard(request):
    if request.method == "POST" and request.POST.get("form_type"):
        form_type = FormTypes(request.POST["form_type"])
        if form_type == FormTypes.REGISTRATIONS:
            reg = AwaitingRegistration.objects.get(
                id=request.POST["awaiting_registration_id"]
            )

            submission = RegistrationRequestApproval(request.POST["submission_type"])

            if submission == RegistrationRequestApproval.APPROVE:
                # TODO: Move this to core app domain logic
                password = User.objects.make_random_password()
                profile = UserProfile(
                    nick=reg.nick,
                    email=reg.email,
                    name_given=reg.name_given,
                    name_family=reg.name_family,
                    gender=reg.gender,
                    # Magic constants to be fixed in the model
                    registration_approved_date=timezone.now(),
                    reputation=0,
                    reputation_available=0,
                    reload="0",
                    status="4",
                    pii_display_permissions=",,,,,,,",
                    level="0",
                    description_raw="Jsem čerstvě zaregistrován...",
                )
                profile.save()

                user = User.objects.create_user(
                    id=profile.id,
                    username=profile.nick,
                    password=password,
                    date_joined=profile.registration_approved_date,
                )
                user.save()
                profile.user = user
                user.save()

                reg.delete()

                send_mail(
                    "Schválení registrace na DraciDoupe.cz",
                    f"Vítejte na DraciDoupe.cz! Vaše heslo {password}, po příhlášení si jej prosím zmeňte. Budeme se těšit!",
                    settings.DDCZ_TRANSACTION_EMAIL_FROM,
                    [reg.email],
                )
                messages.add_message(
                    request, messages.SUCCESS, "Registrace byla schválena"
                )

            elif submission == RegistrationRequestApproval.REJECT:
                reg.delete()

                send_mail(
                    "Zamítnutí registrace na DraciDoupe.cz",
                    "Vše funguje, jak má!",
                    settings.DDCZ_TRANSACTION_EMAIL_FROM,
                    [reg.email],
                )
                messages.add_message(
                    request, messages.SUCCESS, "Registrace byla zamítnuta"
                )

            else:
                messages.error(
                    "Nelze zjistit zda schvalujete nebo zamítate uživatele, zkuste znovu nebo napište zprávcům"
                )

        return HttpResponseRedirect(request.get_full_path())

    registrations = AwaitingRegistration.objects.all().order_by("-date")
    return render(
        request,
        "dashboard.html",
        {
            "registrations": registrations,
            "RegistrationRequestApproval": RegistrationRequestApproval,
            "FormTypes": FormTypes,
        },
    )


@decorators.staff_member_required()
def levelsystem(request):
    """Allows users to configure how level system works"""
    params = LevelSystemParams.objects.all()

    return render(request, "levelsystem/view.html", {"level_params": params})


@decorators.staff_member_required()
def emailtest(request):
    if request.method == "POST":
        profile = UserProfile.objects.get(user_id=request.user.id)
        send_mail(
            "Testovací e-mail redakčního systému DraciDoupe.cz",
            "Vše funguje, jak má!",
            settings.DDCZ_TRANSACTION_EMAIL_FROM,
            [profile.email],
        )
        messages.add_message(
            request, messages.SUCCESS, "Testovací e-mail byl v pořádku odeslán."
        )

    return render(request, "emailtest.html")
