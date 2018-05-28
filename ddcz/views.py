from django.shortcuts import render

from django.http import HttpResponse

from .models import News


def index(request):
    news = News.objects.order_by('-datum')[:10]
    return render(request, 'news/list.html', {'news': news})
