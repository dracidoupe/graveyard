from django.urls import path

from . import views

app_name = "dragon"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("aktuality/", views.news, name="news"),
    path("level-system/", views.levelsystem, name="levelsystem"),
    path("email-test/", views.emailtest, name="emailtest"),
    path("uzivatele/", views.users, name="users"),
    path("uzivatele/<int:user_id>/zablokovat/", views.user_ban, name="user-ban"),
    path("uzivatele/<int:user_id>/odblokovat/", views.user_unban, name="user-unban"),
]
