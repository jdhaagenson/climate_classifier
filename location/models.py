from django.db import models


class PrecipitationData(models.Model):
    Jan = models.FloatField()
    Feb = models.FloatField()
    Mar = models.FloatField()
    Apr = models.FloatField()
    May = models.FloatField()
    Jun = models.FloatField()
    Jul = models.FloatField()
    Aug = models.FloatField()
    Sep = models.FloatField()
    Oct = models.FloatField()
    Nov = models.FloatField()
    Dec = models.FloatField()


class TemperatureData(models.Model):
    Jan = models.FloatField()
    Feb = models.FloatField()
    Mar = models.FloatField()
    Apr = models.FloatField()
    May = models.FloatField()
    Jun = models.FloatField()
    Jul = models.FloatField()
    Aug = models.FloatField()
    Sep = models.FloatField()
    Oct = models.FloatField()
    Nov = models.FloatField()
    Dec = models.FloatField()


class Location(models.Model):
    NORTH = '°N'
    SOUTH = '°S'
    NORTH_AMERICA = 'NA'
    SOUTH_AMERICA = 'SA'
    CENTRAL_AMERICA = 'CA'
    AFRICA = 'AF'
    OCEANIA = 'OC'
    ASIA = 'AS'
    MIDDLE_EAST = 'ME'
    EUROPE = 'EU'
    ANTARCTICA = 'AN'
    REGIONS = [
        (NORTH_AMERICA, 'North America'),
        (SOUTH_AMERICA, 'South America'),
        (CENTRAL_AMERICA, 'Central America'),
        (AFRICA, 'Africa'),
        (OCEANIA, 'Oceania'),
        (ASIA, 'Asia'),
        (MIDDLE_EAST, 'Middle East'),
        (EUROPE, 'Europe'),
        (ANTARCTICA, 'Antarctica')
    ]
    HEMISPHERE_CHOICES = [
        (NORTH, 'N'),
        (SOUTH, 'S')
    ]
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=2, choices=REGIONS)
    precipitation_averages = models.OneToOneField(PrecipitationData, on_delete=models.CASCADE)
    temperature_averages = models.OneToOneField(TemperatureData)
    hemisphere = models.CharField(max_length=1, choices=HEMISPHERE_CHOICES, default='N')



