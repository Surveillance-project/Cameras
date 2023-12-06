from django.urls import path, include
from .views import DistrictListView


urlpatterns = [
    path("v1/districts/city_name/<str:city>", DistrictListView.as_view(), name="districts_list"),
]
