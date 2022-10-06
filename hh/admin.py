from django.contrib import admin
from .models import Regions, Queries, Skills, SkillsArray, Settings


class RegionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'hh_region_id', 'region', 'sort']
    ordering = ('sort', 'region')


class QueriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'region_id', 'query']


class SkillsAdmin(admin.ModelAdmin):
    list_display = ['id', 'skill']


class SkillsArrayAdmin(admin.ModelAdmin):
    list_display = ['id', 'query_id', 'skill_id', 'amount']


admin.site.register(Regions, RegionsAdmin)
admin.site.register(Queries, QueriesAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(SkillsArray, SkillsArrayAdmin)
admin.site.register(Settings)
