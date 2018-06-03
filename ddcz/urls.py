from django.urls import path

from . import views

app_name='ddcz'

urlpatterns = [
    path('', views.index, name='news'),
    path('rubriky/clanky/', views.common_articles, {
        'creative_page_slug': 'clanky'
    }, name='articles-and-essays'),
    path('rubriky/<creative_page_slug>/<int:article_id>-<article_slug>', views.common_article_detail, name='common-article-detail'),
]
