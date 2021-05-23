from django.core.paginator import Paginator
from django.http import (
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from ..commonarticles import (
    SLUG_NAME_TRANSLATION_FROM_CZ,
    COMMON_ARTICLES_CREATIVE_PAGES,
)
from ..forms.comments import PhorumCommentForm, DeletePhorumCommentForm
from ..models import Phorum


@require_http_methods(["GET", "POST"])
def phorum(request):
    if request.method == "POST" and request.POST["post_type"] and request.user:
        if request.POST["post_type"] == "d" and request.POST["submit"] == "Smazat":
            try:
                Phorum.objects.get(
                    id=request.POST["post_id"],
                    nickname=request.user.profile.nick,
                ).delete()
            except Phorum.DoesNotExist as e:
                messages.error(request, "Zprávu se nepodařilo smazat.")
                return HttpResponseRedirect(reverse("ddcz:phorum-list"))

        elif request.POST["post_type"] == "a" and request.POST["submit"] == "Přidej":
            form = PhorumCommentForm(request.POST)
            if form.is_valid():
                Phorum.objects.create(
                    reputation=0,
                    registered_or_ip=1,
                    user=request.user.profile,
                    text=form.cleaned_data["text"],
                    nickname=request.user.profile.nick,
                    email=request.user.profile.email,
                )

        return HttpResponseRedirect(reverse("ddcz:phorum-list"))

    default_limit = 20
    discussions = Phorum.objects.all().order_by("-date")

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
