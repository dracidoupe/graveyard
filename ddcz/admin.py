from django.contrib import admin

from .models import (
    AlchemistTool,
    AwaitingRegistration,
    CommonArticle,
    CreativePageConcept,
    Dating,
    EditorArticle,
    Item,
    Link,
    Monster,
    News,
    ScheduledNotification,
    ScheduledEmail,
    Skill,
    UserProfile,
    RangerSpell,
    WizardSpell,
)

admin.site.site_header = "Administrace pro DraciDoupe.cz"
admin.site.site_title = admin.site.site_header


class SearchableName(admin.ModelAdmin):
    search_fields = ("jmeno",)


class DatingSearch(admin.ModelAdmin):
    search_fields = ("name", "email", "phone", "mobile")


admin.site.register(Dating, DatingSearch)

admin.site.register(AlchemistTool, SearchableName)
admin.site.register(CommonArticle, SearchableName)
admin.site.register(CreativePageConcept, SearchableName)
admin.site.register(Item, SearchableName)
admin.site.register(Link, SearchableName)
admin.site.register(Monster, SearchableName)
admin.site.register(News, SearchableName)
admin.site.register(RangerSpell, SearchableName)
admin.site.register(Skill, SearchableName)
admin.site.register(WizardSpell, SearchableName)

admin.site.register(EditorArticle)

admin.site.register(AwaitingRegistration)
admin.site.register(ScheduledNotification)
admin.site.register(ScheduledEmail)

admin.site.register(UserProfile)
