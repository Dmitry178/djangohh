from django.urls import path
from hh import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('search/', views.search_view, name='search'),
    path('results/', views.results_view, name='results'),
    path('vac/', views.vac_view, name='vac'),
    path('contacts/', views.contacts_view, name='contacts'),
]
