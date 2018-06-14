from django.contrib import admin

from .models import CommonArticle, News

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header

admin.site.register(CommonArticle)
admin.site.register(News)
