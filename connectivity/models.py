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


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    place_of_residence = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"({self.id}) {self.first_name} {self.last_name}"


class CriminalCode(models.Model):
    code = models.CharField()
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"({self.id}) {self.code}| {self.name}"


class CriminalRecord(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    criminal_code_record = models.ForeignKey(CriminalCode, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"({self.id}) {self.criminal_code_record.code} {self.profile.first_name} {self.profile.last_name}"
