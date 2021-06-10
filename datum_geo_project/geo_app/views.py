from django.contrib.gis.geos import Polygon, GEOSGeometry
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_gis.filters import InBBoxFilter
from rest_framework_gis.pagination import GeoJsonPagination

from .models import Country, City, Capital
from .serializers import *
from .base.classes import RetrieveUpdateDestroy


class CountryListView(generics.ListCreateAPIView):
    """Вывод и создание стран"""
    queryset = Country.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CountryListSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True


class CountryView(RetrieveUpdateDestroy):
    """Вывод, обновление ,удаление стран"""
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [permissions.AllowAny]


class CityListView(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вывод и создание городов"""
    queryset = City.objects.all()
    permission_classes = [permissions.AllowAny]
    bbox_filter_field = 'geometry'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True

    def get_serializer_class(self):
        if self.action == 'list':
            return CityListSerializer
        elif self.action == 'create':
            return CityCreateSerializer


class CityView(viewsets.ModelViewSet):
    """Вывод, обновление ,удаление стран"""
    queryset = City.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CityDetailSerializer


class CapitalView(viewsets.ModelViewSet):
    """CRUD Сстолиц"""
    queryset = Capital.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    bbox_filter_field = 'city__geometry'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True

    def get_serializer_class(self):
        if self.action == 'list':
            return CapitalListSerializer
        elif self.action == 'create':
            return CityCreateSerializer
        else:
            return CapitalSerializer


class InsideCountryDataView(generics.ListAPIView):
    """Вывод данных по всем городам, находящимся внутри страны"""

    serializer_class = CityDetailSerializer

    def get_queryset(self):
        instance = Country.objects.get(pk=self.kwargs['pk']).related_city.all()
        return instance


