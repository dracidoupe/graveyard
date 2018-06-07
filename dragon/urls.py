from django.urls import path

from . import views

app_name='dragon'

urlpatterns = [
    path('level-system/', views.levelsystem, name='levelsystem'),
]
