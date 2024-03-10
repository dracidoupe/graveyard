from django.conf import settings
from django.urls import path, re_path
from django.views.generic.base import RedirectView, TemplateView

from . import views
from .views import news, tavern, misc, email
from .views.legacy import legacy_router, print_legacy_router

app_name = "ddcz"

urlpatterns = [
    path("", RedirectView.as_view(url="aktuality/", permanent=False)),
    ### Legacy redirects from stare.dracidoupe.cz
    path("index.php", legacy_router, name="legacy-router"),
    re_path(
        "code/(?P<page_category>[a-zA-Z0-9_-]+)/(?P<page_category_second>[a-zA-Z0-9_-]+)_tisk.php",
        print_legacy_router,
        name="legacy-router-print",
    ),
    re_path(
        r"^ikonky/(?P<file>.+)$",
        RedirectView.as_view(url=f"{settings.USER_ICON_MEDIA_ROOT_URL}%(file)s"),
        name="redirect_ikonky",
    ),
    ### Common pages for bots etc.
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "ads.txt",
        TemplateView.as_view(template_name="ads.txt", content_type="text/plain"),
    ),
    path(
        ".well-known/security.txt",
        TemplateView.as_view(template_name="security.txt", content_type="text/plain"),
    ),
    # Prefetch for Google Chrome
    # Courtesy of https://webmasters.stackexchange.com/a/139570
    path(
        ".well-known/traffic-advice",
        TemplateView.as_view(
            template_name="traffic-advice.json",
            content_type="application/trafficadvice+json",
        ),
    ),
    ### Creations and Creative Pages
    path(
        "rubriky/<creative_page_slug>/", views.creative_page_list, name="creation-list"
    ),
    path(
        "rubriky/<creative_page_slug>/koncepce/",
        views.creative_page_concept,
        name="creative-page-concept",
    ),
    path(
        "rubriky/<creative_page_slug>/kontrola-html/",
        views.creative_page_html_check,
        name="creative_page_html_check",
    ),
    # path(
    #     "rubriky/<creative_page_slug>/<int:creation_id>-<creation_slug>/",
    #     views.creation_detail,
    #     name="creation-detail",
    # ),
    re_path(
        "^rubriky/(?P<creative_page_slug>\w+)/(?P<creation_id>\d+)-(?P<creation_slug>[a-zA-Z0-9_-]+)/$",
        views.creation_detail,
        name="creation-detail",
    ),
    re_path(
        "rubriky/(?P<creative_page_slug>\w+)/(?P<creation_id>\d+)-(?P<creation_slug>[a-zA-Z0-9_-]+)/obr_pris/(?P<image_path>.+)",  # /(?P<image_path_name>\w+)",
        views.creation_detail_image,
        name="creation-detail-image",
    ),
    # Standard list and detail are under creation pages above,
    # Those are for executing redirect to download/quest location
    path("download/<int:download_id>/", views.download_file, name="download-file"),
    path(
        "dobrodruzstvi/<int:quest_id>/",
        views.quest_view_redirect,
        name="quest-view-legacy-redirect",
    ),
    re_path(
        "dobrodruzstvi/(?P<quest_id>\d+)-(?P<quest_slug>[a-zA-Z0-9_-]+)/$",
        views.quest_view_redirect,
        name="quest-view",
    ),
    ### User handling
    path("uzivatele/", views.users_list, name="users-list"),
    path("uzivatel/prihlaseni/", views.login, name="login-action"),
    path("registrace/", views.sign_up, name="sign-up"),
    path("uzivatel/odhlaseni/", views.logout, name="logout-action"),
    path(
        "uzivatel/reset-hesla/",
        views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "uzivatel/reset-hesla/hotovo/",
        views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "uzivatel/zmena-hesla/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password-change",
    ),
    path(
        "uzivatel/zmena-hesla/hotovo/",
        views.PasswordResetCompleteView.as_view(),
        name="password-change-done",
    ),
    path(
        "uzivatel/<int:user_profile_id>-<nick_slug>/",
        views.user_profile,
        name="user-detail",
    ),
    path("autor/<int:author_id>-<slug>/", views.author_detail, name="author-detail"),
    ### User settings
    path("nastaveni/zmena-skinu/", views.change_skin, name="change-skin"),
    ### Emails
    path(
        "e-mail/antispam/potvrzeni/",
        TemplateView.as_view(template_name="emails/unsub-confirm.html"),
        name="email-antispam-confirm",
    ),
    path(
        "e-mail/antispam/<email_base64>-<unsub_token>/",
        email.antispam,
        name="email-antispam",
    ),
    ### Info sites
    path("aktuality/", news.list, name="news"),
    path("novinky/", news.newsfeed, name="newsfeed"),
    path("seznamka/", views.dating, name="dating"),
    path("inzerce/", views.market, name="market"),
    path("linky/", views.links, name="links-list"),
    ### Discussions & Tavern
    path("forum/", views.phorum, name="phorum-list"),
    path("putyka/", tavern.list_tables, name="tavern-list"),
    path(
        "putyka/stul/<int:tavern_table_id>/prispevky/",
        tavern.table_posts,
        name="tavern-posts",
    ),
    path(
        "putyka/stul/<int:tavern_table_id>/nastenka/",
        tavern.notice_board,
        name="tavern-notice-board",
    ),
    path(
        "putyka/stul/<int:tavern_table_id>/administrace/",
        tavern.table_administration,
        name="tavern-table-admin",
    ),
    path(
        "putyka/stul/<int:tavern_table_id>/oblibit/",
        tavern.table_bookmark,
        name="tavern-bookmark",
    ),
    ### Static Editorial Pages
    ### Would be easier to give them /static prefix, but it makes for ugly URL
    path(
        "co-je-draci-doupe/",
        views.editor_article,
        name="about-drd",
        kwargs={"slug": "co-je-draci-doupe"},
    ),
    path(
        "draci-manual/",
        views.editor_article,
        name="website-manual",
        kwargs={"slug": "draci-manual"},
    ),
    path(
        "otazky-a-odpovedi/",
        views.editor_article,
        name="faq",
        kwargs={"slug": "otazky-a-odpovedi"},
    ),
    path(
        "tvurci-a-redakce/",
        misc.web_authors_and_editors,
        name="web-authors-and-editors",
    ),
    path("posta/", views.postal_service, name="postal-service"),
]
