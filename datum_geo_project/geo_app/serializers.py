from rest_framework import serializers
from PIL import Image
from rest_framework_gis.fields import GeometrySerializerMethodField

from .models import City, Country, Capital
from rest_framework_gis.serializers import GeoModelSerializer, GeoFeatureModelSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]

            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class CityListSerializer(GeoFeatureModelSerializer):
    # country = serializers.ReadOnlyField(source='country.name')
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        geo_field = 'geometry'
        model = City
        fields = ('name', 'country', 'geometry')


class CityCreateSerializer(GeoModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityDetailSerializer(GeoFeatureModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

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
    related_city = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Country
        geo_field = 'location'
        fields = ('id', 'name', 'location', 'related_city')


class CapitalListSerializer(GeoModelSerializer):
    city = CityListSerializer()

    class Meta:
        model = Capital
        fields = ('id', 'city')


class CapitalCreateSerializer(GeoModelSerializer):
    city = CityDetailSerializer()

    def create(self, validated_data):
        city = City.objects.create(**dict(validated_data['city']))
        capital = Capital.objects.create(city_id=city.id)
        return capital

    class Meta:
        model = Capital
        fields = ('id', 'city')


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
