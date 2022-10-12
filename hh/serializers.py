# from django.conf.urls import url, include
from .models import Regions, Queries, Skills
from rest_framework import routers, serializers, viewsets


class RegionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Regions
        exclude = ['sort']


class QueriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Queries
        exclude = ['scan_date']  # не реализовано


class SkillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'
