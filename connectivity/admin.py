from django.contrib import admin
from . import models

models_to_register = [
    models.Camera,
    models.CameraCluster,
    models.District,
    models.City,
    models.Country,
    models.Street,
]

for model in models_to_register:
    admin.site.register(model)
