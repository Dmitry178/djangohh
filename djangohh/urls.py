from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hh.api_views import RegionsViewSet, QueriesViewSet, SkillsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'regions', RegionsViewSet)
router.register(r'queries', QueriesViewSet)
router.register(r'skills', SkillsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('hh.urls', 'djangohh'), namespace='djangohh')),
    path('users/', include('userapp.urls', namespace='users')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v0/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
