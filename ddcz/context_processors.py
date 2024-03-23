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

    if skin == "historic":
        logo_width = "475px"
        logo_height = "175px"
    else:
        logo_width = "600px"
        logo_height = "87.2px"

    return {
        "user": request.user,
        "ddcz_profile": request.ddcz_profile,
        "skin": skin,
        "skin_for_include": skin_directory,
        "current_page_url": request.get_full_path(),
        "skin_css_url": staticfiles_storage.url(
            "skins/%(skin)s/css/main.css" % {"skin": skin}
        ),
        "skin_favico_url": staticfiles_storage.url(
            "skins/%(skin)s/img/drak.ico" % {"skin": skin}
        ),
        "skin_logo_url": staticfiles_storage.url("skins/%s/img/logo.svg" % skin),
        "logo_width": logo_width,
        "logo_height": logo_height,
        "login_form": LoginForm(),
        "discord_invite_link": settings.DISCORD_INVITE_LINK,
        "bugfix_tavern_table_id": settings.BUGFIX_TAVERN_TABLE_ID,
        "deploy_info_html": deploy_info_html,
    }
