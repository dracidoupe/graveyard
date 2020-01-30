from django.contrib import admin

from .models import CommonArticle, Monster, News, CreativePageConcept

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header

admin.site.register(CommonArticle)
admin.site.register(Monster)
admin.site.register(News)
admin.site.register(CreativePageConcept)
