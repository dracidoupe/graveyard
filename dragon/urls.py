from django.urls import path

from . import views

app_name = "dragon"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("aktuality/", views.news, name="news"),
    path("level-system/", views.levelsystem, name="levelsystem"),
    path("email-test/", views.emailtest, name="emailtest"),
]
