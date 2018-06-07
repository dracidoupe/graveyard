from django.contrib import admin

from .models import *

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header

admin.site.register(CommonArticles)
admin.site.register(News)
