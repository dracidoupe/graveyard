from django.urls import path

from . import views

app_name = "dragon"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("level-system/", views.levelsystem, name="levelsystem"),
]
