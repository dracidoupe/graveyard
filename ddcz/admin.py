from django.contrib import admin

from .models import (
    AlchemistTool,
    CommonArticle, CreativePageConcept,
    Item, Link, Monster, News, Skill,
    RangerSpell, WizardSpell
)

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header

class SearchableAdmin(admin.ModelAdmin):
    search_fields = ('jmeno',)


admin.site.register(AlchemistTool, SearchableAdmin)
admin.site.register(CommonArticle, SearchableAdmin)
admin.site.register(CreativePageConcept, SearchableAdmin)
admin.site.register(Item, SearchableAdmin)
admin.site.register(Link, SearchableAdmin)
admin.site.register(Monster, SearchableAdmin)
admin.site.register(News, SearchableAdmin)
admin.site.register(RangerSpell, SearchableAdmin)
admin.site.register(Skill, SearchableAdmin)
admin.site.register(WizardSpell, SearchableAdmin)
