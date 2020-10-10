from django.urls import path
from django.views.generic.base import RedirectView


from . import views

app_name='ddcz'

urlpatterns = [
    path('', RedirectView.as_view(url='aktuality/', permanent=True)),
    path('aktuality/', views.index, name='news'),
    path('rubriky/<creative_page_slug>/', views.creative_page_list, name='common-article-list'),
    path('rubriky/<creative_page_slug>/koncepce/', views.creative_page_concept, name='creative-page-concept'),
    path('rubriky/<creative_page_slug>/<int:article_id>-<article_slug>/', views.creation_detail, name='common-article-detail'),

    path('seznamka/', views.dating, name='dating'),

    path('linky/', views.links, name='links-list'),

    path('nastaveni/zmena-skinu/', views.change_skin, name='change-skin'),
    path('uzivatel/prihlaseni/', views.login, name='login-action'),
    path('uzivatel/odhlaseni/', views.logout, name='logout-action'),
    path('uzivatel/reset-hesla/', views.PasswordResetView.as_view(), name='password-reset'),
    path('uzivatel/reset-hesla/hotovo/', views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('uzivatel/zmena-hesla/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-change'),
    path('uzivatel/zmena-hesla/hotovo/', views.PasswordResetCompleteView.as_view(), name='password-change-done'),
    path('uzivatel/<int:user_profile_id>-<nick_slug>/', views.user_profile, name='user-detail'),
]
