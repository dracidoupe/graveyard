from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name='ddcz'

urlpatterns = [
    path('', RedirectView.as_view(url='aktuality/', permanent=True)),
    path('aktuality/', views.index, name='news'),
    path('rubriky/<creative_page_slug>/', views.common_articles, name='common-article-list'),
    path('rubriky/<creative_page_slug>/<int:article_id>-<article_slug>/', views.common_article_detail, name='common-article-detail'),

    path('seznamka/', views.dating, name='dating'),

    path('nastaveni/zmena-skinu/', views.change_skin, name='change-skin'),
    path('uzivatel/prihlaseni/', views.login, name='login-action'),
    path('uzivatel/odhlaseni/', views.logout, name='logout-action'),
]
