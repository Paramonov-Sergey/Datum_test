from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *


class CountryAdmin(LeafletGeoAdmin):
    list_display = ('name','location')


class CityAdmin(LeafletGeoAdmin):
    list_display = ('name','geometry')


# class CapitalAdmin(LeafletGeoAdmin):
#     list_display = ('name',)


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Capital)
