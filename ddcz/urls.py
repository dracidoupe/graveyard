from django.urls import path

from . import views

app_name='ddcz'

urlpatterns = [
    path('', views.index, name='news'),
]
