from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

from .forms.authentication import LoginForm


def common_variables(request):
    skin = request.session.get("skin", "light")
    skin_directory = skin if skin not in ["light", "dark"] else "light-dark"
    return {
        "user": request.user,
        "skin": skin,
        "skin_for_include": skin_directory,
        "current_page_url": request.get_full_path(),
        "skin_css_url": staticfiles_storage.url(
            "skins/%(skin)s/main.css" % {"skin": skin}
        ),
        "skin_favico_url": staticfiles_storage.url(
            "skins/%(skin)s/img/drak.ico" % {"skin": skin}
        ),
        "skin_logo_url": staticfiles_storage.url("skins/%s/img/logo.gif" % skin),
        "login_form": LoginForm(),
        "discord_invite_link": settings.DISCORD_INVITE_LINK,
    }
