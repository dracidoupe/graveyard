import logging

from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..email import validate_unsubscribe_token, blacklist_email
from ..models import UnsubscribedEmail

logger = logging.getLogger(__name__)


@require_http_methods(["HEAD", "GET", "POST"])
def antispam(request, email_base64, unsub_token):
    if not email_base64 or not unsub_token:
        return HttpResponseBadRequest("Špatný formát odhlašovacího kódu.")

    try:
        validate_unsubscribe_token(email_base64, unsub_token)
    except UnsubscribedEmail.DoesNotExist:
        logger.warning(
            f"User tried to unsubscribe email {email_base64}, but it wasn't found in a database"
        )
        return HttpResponseBadRequest(
            "Tento e-mail není v databázi. Nezměnil jsi ho mezitím v profilu, případně nebyl už zařazen do seznamu zakázaných e-mailů? Byla zaslána zpráva adminům, neb toto by se nemělo stát. "
        )
    else:
        if request.method == "POST":
            blacklist_email(email_base64)
            return HttpResponseRedirect(reverse("ddcz:email-antispam-confirm"))
        else:
            return render(
                request,
                "emails/antispam.html",
                {},
            )
