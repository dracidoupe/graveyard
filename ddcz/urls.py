from django.urls import path

from . import views

app_name='ddcz'

urlpatterns = [
    path('', views.index, name='news'),
    path('rubriky/<creative_page_slug>/', views.common_articles, name='common-article-list'),
    path('rubriky/<creative_page_slug>/<int:article_id>-<article_slug>/', views.common_article_detail, name='common-article-detail'),

    path('seznamka/', views.dating, name='dating'),

    path('nastaveni/zmena-skinu/', views.change_skin, name='change-skin'),

]
