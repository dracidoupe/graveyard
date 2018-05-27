from django.shortcuts import render

from django.http import HttpResponse

from .models import Aktuality


def index(request):
    akt = Aktuality.objects.all()[0]
    return HttpResponse("<html><head><meta charset=\"utf-8\"><title>Test</title></head><body>{0}</body></html>".format(akt.text))
