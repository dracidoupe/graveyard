from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..forms.comments import PhorumCommentForm, DeletePhorumCommentForm
from ..models import Phorum
from ..text import escape_user_input


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
                    text=escape_user_input(form.cleaned_data["text"]),
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
