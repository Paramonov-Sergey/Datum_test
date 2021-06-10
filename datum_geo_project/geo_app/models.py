from django.contrib.gis.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    location = models.MultiPolygonField(srid=4326, null=False, blank=False)

    def __str__(self):
        return f'Country : {self.name} cordinates : {self.location}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='cities/', verbose_name='Изображение', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Country', on_delete=models.SET_NULL, null=True,
                                related_name='related_city')

    geometry = models.PolygonField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Capital(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='related_capital')

    def __str__(self):
        return self.city.name

    class Meta:
        verbose_name = 'Столица'
        verbose_name_plural = 'Столицы'
