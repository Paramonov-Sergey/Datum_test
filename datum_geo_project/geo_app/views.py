from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework_gis.filters import InBBoxFilter
from .models import Country, City, Capital
from .serializers import *
from .base.classes import RetrieveUpdateDestroy, ListCreateGenericViewSet


class CountryListView(generics.ListCreateAPIView):
    """Вывод и создание стран"""
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer
    bbox_filter_field = 'location'
    filter_backends = (InBBoxFilter,)
    # bbox_filter_include_overlapping = True


class CountryView(RetrieveUpdateDestroy):
    """Вывод, обновление ,удаление стран"""
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CityListView(ListCreateGenericViewSet):
    """Вывод и создание городов"""
    queryset = City.objects.all()
    bbox_filter_field = 'geometry'
    filter_backends = (InBBoxFilter,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CityListSerializer
        elif self.action == 'create':
            return CityCreateSerializer


class CityView(viewsets.ModelViewSet):
    """Вывод, обновление ,удаление стран"""
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer
    parser_classes = [MultiPartParser, ]


class CapitalView(viewsets.ModelViewSet):
    """CRUD Столиц"""
    queryset = Capital.objects.all()
    pagination_class = PageNumberPagination
    bbox_filter_field = 'city__geometry'
    filter_backends = (InBBoxFilter,)
    serializer_by_action = {'list': CapitalListSerializer, 'create': CapitalCreateSerializer}

    def get_serializer_class(self):
        try:
            return self.serializer_by_action[self.action]
        except KeyError:
            return CapitalSerializer


class InsideCountryDataView(generics.ListAPIView):
    """Вывод данных по всем городам, находящимся внутри страны"""

    serializer_class = CityDetailSerializer

    def get_queryset(self):
        instance = Country.objects.get(pk=self.kwargs['pk']).related_city.all()
        return instance


class SumAreaView(generics.GenericAPIView):
    pass
