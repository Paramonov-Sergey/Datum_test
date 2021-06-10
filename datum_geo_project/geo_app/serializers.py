from rest_framework import serializers
from rest_framework_gis.fields import GeometrySerializerMethodField

from .models import City, Country, Capital
from rest_framework_gis.serializers import GeoModelSerializer, GeoFeatureModelSerializer


class CityListSerializer(GeoFeatureModelSerializer):
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        geo_field = 'geometry'
        model = City
        fields = ('name', 'country', 'geometry')


class CityCreateSerializer(GeoModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityDetailSerializer(GeoFeatureModelSerializer):
    class Meta:
        geo_field = 'geometry'
        model = City
        fields = '__all__'


class CountryListSerializer(GeoFeatureModelSerializer):
    class Meta:
        geo_field = 'location'
        model = Country
        fields = ('id', 'name', 'location')


class CountrySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Country
        geo_field = 'location'
        fields = ('id', 'name', 'location', 'related_city')


class CapitalListSerializer(GeoModelSerializer):
    city = CityListSerializer()

    class Meta:
        model = Capital
        fields = ('id', 'city',)


class CapitalCreateSerializer(GeoModelSerializer):
    city = CityDetailSerializer()

    def create(self, validated_data):
        city = City.objects.create(**dict(validated_data['city']))
        capital = Capital.objects.create(city_id=city.id)
        return capital

    class Meta:
        model = Capital
        fields = ('id', 'city',)


class CapitalSerializer(GeoModelSerializer):
    city = CityDetailSerializer()

    class Meta:
        model = Capital
        fields = ('city',)

    def update(self, instance, validated_data):
        city = City.objects.get(id=instance.city.id)
        city.name = dict(validated_data['city']).get('name')
        city.geometry = dict(validated_data['city']).get('geometry')
        city.description = dict(validated_data['city']).get('description')
        city.image = dict(validated_data['city']).get('image', city.image)
        city.country = dict(validated_data['city']).get('country', city.country)
        city.save()
        return instance


class InsideCountrySerializer(GeoFeatureModelSerializer):
    related_city = CityDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ('related_city',)
