from django.db import models

COUNTRY_MAX_CHARS = 90
CITY_MAX_CHARS = 189
DISTRICT_MAX_CHARS = 150
STREET_MAX_CHARS = 150


class Country(models.Model):
    name = models.CharField(max_length=COUNTRY_MAX_CHARS, unique=True, )

    def __str__(self):
        return f"({self.id}) {self.name}"


class City(models.Model):
    name = models.CharField(max_length=CITY_MAX_CHARS, unique=True)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}) {self.name} | {self.country.name}"


class District(models.Model):
    name = models.CharField(max_length=DISTRICT_MAX_CHARS, unique=True)
    city = models.ForeignKey("City", on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}) {self.name} | {self.city.name}"


class Street(models.Model):
    name = models.CharField(max_length=STREET_MAX_CHARS, unique=True)
    district = models.ForeignKey("District", on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}) {self.name} | {self.district.name}"


class CameraCluster(models.Model):
    name = models.CharField(max_length=80, null=True)
    district = models.OneToOneField("District", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"cluster_{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"({self.id}) {self.name} | {self.district.name}"


class Camera(models.Model):
    # Camera id from producer service
    camera_id = models.BigIntegerField(unique=True)
    camera_cluster = models.ForeignKey(CameraCluster, on_delete=models.CASCADE)
    clearance_level = models.IntegerField(default=1)

    def __str__(self):
        return (f"({self.id}) {self.camera_id} | clearance: {self.clearance_level}" +
                f" | {self.camera_cluster.name}")
