from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views import decorators
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from ddcz.models import LevelSystemParams, UserProfile, AwaitingRegistration, News
from ddcz.notifications import NotificationEvent, schedule_notification, Audience

from .forms.dashboard import FormTypes
from .forms.users import RegistrationRequestApproval
from .forms.news import News as NewsForm


@decorators.staff_member_required()
def dashboard(request):
    if request.method == "POST" and request.POST.get("form_type"):
        form_type = FormTypes(request.POST["form_type"])
        if form_type == FormTypes.REGISTRATIONS:
            reg = AwaitingRegistration.objects.get(
                id=request.POST["awaiting_registration_id"]
            )

            submission = RegistrationRequestApproval(request.POST["submission_type"])
            message = request.POST["message"]
            if message:
                message = (
                    f"\nKapitán studující tvé lejstro k tomu poznamenal: {message}\n"
                )

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

                # TODO: Registration and user should not be deleted until email is sent so in case of
                # email failure, there is a way to retry
                # That said, sort it out when doing notification framework
                # TODO: Properly sent and design both HTML and plain text version
                # see https://stackoverflow.com/questions/2809547/creating-email-templates-with-django

                send_mail(
                    "Schválení registrace na DraciDoupe.cz",
                    f"""Vítejte na DraciDoupe.cz!

                    Vaše heslo je {password}, po příhlášení si jej prosím zmeňte v sekci Nastavení. Doporučujeme též k přečetení Dračí Manuál a Otázky a Odpovědi. Můžete se též přidat na náš Discord server {settings.DISCORD_INVITE_LINK} .
                    {message}
                    Děkujeme za Vaši registraci a doufáme, že se vám ve Městě bude líbit.

                    — Redakce a vývojový tým DraciDoupe.cz
                    """,
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
                    f"""Zdravíme,

                    Vaše žádost o registraci na DraciDoupe.cz byla bohužel zamítnuta. Pokud máte pocit, že se tak stalo neprávem, můžete se zeptat na podrobnosti na našem Discord serveru na {settings.DISCORD_INVITE_LINK} .
                    {message}
                    I přes toto nedorozumění Vám přejeme příjemný den,

                    — Redakce a vývojový tým DraciDoupe.cz
                    """,
                    # TODO: editor email so there is contact?
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
def news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            added_news = News.objects.create(
                text=form.cleaned_data["text"],
                date=timezone.now(),
                author=request.ddcz_profile.nick,
                author_mail=request.ddcz_profile.email,
            )
            schedule_notification(
                event=NotificationEvent.NEWS_ADDED,
                affected_object=added_news,
                extra_data={
                    "audience": Audience[form.cleaned_data["audience"]].value,
                    "author_nick": request.ddcz_profile.nick,
                },
            )
            messages.success(request, "Aktualita přidána a připravena k odeslání")
            return HttpResponseRedirect(request.get_full_path())

    else:
        form = NewsForm()

    return render(request, "news.html", {"form": form})


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
            request,
            messages.SUCCESS,
            f"Testovací e-mail byl v pořádku odeslán na {profile.email}.",
        )

    return render(request, "emailtest.html")
