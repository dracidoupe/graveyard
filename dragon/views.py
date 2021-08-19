from django.conf import settings
from django.contrib.admin.views import decorators
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render

from ddcz.models import LevelSystemParams, UserProfile


@decorators.staff_member_required()
def dashboard(request):

    return render(request, "dashboard.html", {})


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
