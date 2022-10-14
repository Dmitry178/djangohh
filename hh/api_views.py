from .models import Regions, Queries, Skills, SkillsArray
from .serializers import RegionsSerializer, QueriesSerializer, SkillsSerializer, SkillsArraySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .permissions import ReadOnly, AuthReadOnly


class RegionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated | ReadOnly]
    queryset = Regions.objects.all()
    serializer_class = RegionsSerializer


class QueriesViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser | AuthReadOnly]
    queryset = Queries.objects.all()
    serializer_class = QueriesSerializer


class SkillsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | AuthReadOnly]
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


class SkillsArrayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | AuthReadOnly]
    queryset = SkillsArray.objects.all()
    serializer_class = SkillsArraySerializer
