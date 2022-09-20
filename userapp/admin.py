from django.contrib import admin
from .models import HhUser, UsersQueries

# Register your models here.
admin.site.register(HhUser)
admin.site.register(UsersQueries)
