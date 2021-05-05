from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

from .forms.authentication import LoginForm


def common_variables(request):
    skin = request.session.get("skin", "light")
    skin_directory = skin if skin not in ["light", "dark"] else "light-dark"
    deploy_info_html = settings.DEPLOY_VERSION
    if settings.DEPLOY_HASH:
        deploy_info_html = f'{deploy_info_html} (<a href="https://github.com/dracidoupe/graveyard/commit/{settings.DEPLOY_HASH}">{settings.DEPLOY_HASH}</a>)'
    if settings.DEPLOY_DATE:
        deploy_info_html = f"{deploy_info_html} ze dne {settings.DEPLOY_DATE}"

    return {
        "user": request.user,
        "ddcz_profile": request.ddcz_profile,
        "skin": skin,
        "skin_for_include": skin_directory,
        "current_page_url": request.get_full_path(),
        "skin_css_url": staticfiles_storage.url(
            "skins/%(skin)s/main.css" % {"skin": skin}
        ),
        "skin_favico_url": staticfiles_storage.url(
            "skins/%(skin)s/img/drak.ico" % {"skin": skin}
        ),
        "skin_logo_url": staticfiles_storage.url("skins/%s/img/logo.svg" % skin),
        "login_form": LoginForm(),
        "discord_invite_link": settings.DISCORD_INVITE_LINK,
        "deploy_info_html": deploy_info_html,
    }
