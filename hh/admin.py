from django.contrib import admin
from .models import Regions, Queries, Skills, SkillsArray, Settings

admin.site.register(Regions)
admin.site.register(Queries)
admin.site.register(Skills)
admin.site.register(SkillsArray)
admin.site.register(Settings)