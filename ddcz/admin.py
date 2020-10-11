from django.contrib import admin

from .models import (
    AlchemistTool,
    CommonArticle, CreativePageConcept,
    Monster, News, Skill
)

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header

class CommonArticleAdmin(admin.ModelAdmin):
    search_fields = ('jmeno',)

class AlchemistToolAdmin(admin.ModelAdmin):
    search_fields = ('jmeno',)


admin.site.register(AlchemistTool, AlchemistToolAdmin)
admin.site.register(CommonArticle, CommonArticleAdmin)
admin.site.register(CreativePageConcept)
admin.site.register(Monster)
admin.site.register(News)
admin.site.register(Skill)
