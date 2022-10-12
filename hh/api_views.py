from .models import Regions, Queries, Skills
from .serializers import RegionsSerializer, QueriesSerializer, SkillsSerializer
from rest_framework import viewsets


class RegionsViewSet(viewsets.ModelViewSet):
    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer


class QueriesViewSet(viewsets.ModelViewSet):
    queryset = Queries.objects.all()
    serializer_class = QueriesSerializer


class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
