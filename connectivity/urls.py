from django.urls import path, include
from .views import DistrictListView, ClusterView, ListClustersWithLocationView


urlpatterns = [
    path("v1/districts/city_name/<str:city>", DistrictListView.as_view(), name="districts_list"),
    path("v1/clusters/<int:id>", ClusterView.as_view(), name="cluster"),
    path("v1/clusters", ListClustersWithLocationView.as_view(), name="cluster_list"),
    path("v1/clusters/<str:camera_cluster_name>", ClusterView.as_view(), name="cluster_by_name"),
]
