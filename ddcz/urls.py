from django.urls import path
from django.views.generic.base import RedirectView


from . import views

app_name='ddcz'

urlpatterns = [
    path('', RedirectView.as_view(url='aktuality/', permanent=True)),
    path('aktuality/', views.index, name='news'),
    path('rubriky/<creative_page_slug>/', views.creative_page_list, name='creation-list'),
    path('rubriky/<creative_page_slug>/koncepce/', views.creative_page_concept, name='creative-page-concept'),
    path('rubriky/<creative_page_slug>/<int:creation_id>-<creation_slug>/', views.creation_detail, name='creation-detail'),

    # Standard list and detail are under creation pages above,
    # Those are for executing redirect to download/quest location
    path('download/<int:download_id>/', views.download_file, name='download-file'),
    path('dobrodruzstvi/<int:quest_id>/', views.quest_view_redirect, name='quest-view'),

    path('seznamka/', views.dating, name='dating'),

    path('linky/', views.links, name='links-list'),

    path('nastaveni/zmena-skinu/', views.change_skin, name='change-skin'),

    path('autor/<int:author_id>-<slug>/', views.author_detail, name='author-detail'),

    path('uzivatel/prihlaseni/', views.login, name='login-action'),
    path('uzivatel/odhlaseni/', views.logout, name='logout-action'),
    path('uzivatel/reset-hesla/', views.PasswordResetView.as_view(), name='password-reset'),
    path('uzivatel/reset-hesla/hotovo/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('uzivatel/zmena-hesla/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-change'),
    path('uzivatel/zmena-hesla/hotovo/', views.PasswordResetCompleteView.as_view(), name='password-change-done'),
    path('uzivatel/<int:user_profile_id>-<nick_slug>/', views.user_profile, name='user-detail'),

    path('forum/', views.phorum, name='phorum-list'),

]
