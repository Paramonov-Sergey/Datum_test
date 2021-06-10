from django.urls import path
from .views import *

country_detail = CountryView.as_view(
    actions={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

city_list = CityListView.as_view(actions={'get': 'list', 'post': 'create'})

city_detail = CityView.as_view(
    actions={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

capital_list = CapitalView.as_view(actions={'get': 'list', 'post': 'create'})

capital_detail = CapitalView.as_view(
    actions={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('country/', CountryListView.as_view(), name='list-country'),
    path('country/<int:pk>/', country_detail, name='country-detail'),
    path('city/', city_list, name='list-city'),
    path('city/<int:pk>/', city_detail, name='city-detail'),
    path('capital/', capital_list, name='list-capital'),
    path('capital/<int:pk>/', capital_detail, name='capital-detail'),

    path('country_data/<int:pk>/', InsideCountryDataView.as_view(), name='country-info'),

]
