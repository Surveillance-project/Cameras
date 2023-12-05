import uuid

from django.db import models


COUNTRY_MAX_CHARS = 90
CITY_MAX_CHARS = 189
DISTRICT_MAX_CHARS = 150
STREET_MAX_CHARS = 150


class Country(models.Model):
    name = models.CharField(max_length=COUNTRY_MAX_CHARS, unique=True,)


class City(models.Model):
    name = models.CharField(max_length=CITY_MAX_CHARS, unique=True)
    country = models.OneToOneField("Country", on_delete=models.CASCADE)


class District(models.Model):
    name = models.CharField(max_length=DISTRICT_MAX_CHARS, unique=True)
    city = models.OneToOneField("City", on_delete=models.CASCADE)


class Street(models.Model):
    name = models.CharField(max_length=STREET_MAX_CHARS, unique=True)
    district = models.OneToOneField("District", on_delete=models.CASCADE)


class CameraCluster(models.Model):
    name = models.CharField(max_length=80, default=f"cluster_{CameraCluster.id}")
    district = models.OneToOneField("District", on_delete=models.CASCADE)


class Camera(models.Model):
    # Camera id from producer service
    camera_id = models.BigIntegerField(unique=True)
    clearance_level = models.IntegerField(default=1)
