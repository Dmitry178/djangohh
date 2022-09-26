from django.urls import path
from hh import views

app_name = 'hh'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_view, name='search'),
    path('results/', views.results_view, name='results'),
    path('vac/<int:vac_id>/', views.vac_view, name='vac'),
    path('history/', views.history_view, name='history'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('region-list', views.RegionsListView.as_view(), name='region_list'),
    path('region-detail/<int:pk>/', views.RegionsDetailView.as_view(), name='region_detail'),
    path('region-create/', views.RegionsCreateView.as_view(), name='region_create'),
    path('region-update/<int:pk>/', views.RegionsUpdateView.as_view(), name='region_update'),
    path('region-delete/<int:pk>/', views.RegionsDeleteView.as_view(), name='region_delete'),
]
