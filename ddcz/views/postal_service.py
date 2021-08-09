import logging
from datetime import datetime

from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from ..text import escape_user_input
from ..models import UserProfile, Letters

FORM_DELETE = 1
FORM_SEND = 2
FORM_REPLY = 4

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["HEAD", "GET", "POST"])
def postal_service(request):
    if request.method == "POST":

        fid = int(request.POST.get("fid"))
        if fid == FORM_SEND:

            try:
                Letters.objects.create(
                    receiver=UserProfile.objects.get(id=request.POST.get("whom")).nick,
                    sender=request.user.userprofile.nick,
                    text=request.POST.get("text"),
                    date=datetime.now(),
                    visibility=1,
                )
                return HttpResponseRedirect(reverse("ddcz:postal-service"))

            except UserProfile.DoesNotExist:
                id = request.POST.get("whom")
                logger.error(
                    f"A message between user has been submitted but the receiver of userprofile can not be found in our database. ID: {id}"
                )

        elif fid == FORM_DELETE:

            try:
                letter = Letters.objects.filter(pk=request.POST.get("id", 0)).update(
                    visibility=0
                )
                return HttpResponseRedirect(reverse("ddcz:postal-service"))

            except Letters.DoesNotExist:
                id = request.POST.get("id")
                user = request.user.userprofile.nick
                logger.error(
                    f"There has been an attempt to delete a message with non existing id: {id}, User: {user}"
                )
                return HttpResponseRedirect(reverse("ddcz:postal-service"))

    nick = request.user.userprofile.nick
    offset = int(request.GET.get("s", 1)) - 1
    limit = int(request.GET.get("l", 50))
    letters = Letters.objects.filter(
        (Q(receiver=nick) | Q(sender=nick)) & Q(visibility=1)
    ).order_by("-date")[offset:limit]
    box_occupancy = Letters.objects.filter(
        (Q(receiver=nick) | Q(sender=nick)) & Q(visibility=1)
    ).count()

    return render(
        request,
        "postal_service/postal_office.html",
        {
            "reply_id": FORM_REPLY,
            "send_id": FORM_SEND,
            "delete_id": FORM_DELETE,
            "users": UserProfile.objects.all(),
            "letters": letters,
            "box_occupancy": box_occupancy,
        },
    )
