from django.urls import path, include
from .views import DistrictListView, ClusterView, ListClustersWithLocationView, CameraView, ImageFilterView, ReportView, GetCamerasView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("v1/districts/city_name/<str:city>", DistrictListView.as_view(), name="districts_list"),
    path("v1/clusters/<int:id>", ClusterView.as_view(), name="cluster"),
    path("v1/clusters", ListClustersWithLocationView.as_view(), name="cluster_list"),
    path("v1/clusters/<str:camera_cluster_name>", ClusterView.as_view(), name="cluster_by_name"),
    path("v1/cameras/<int:pk>", CameraView.as_view(), name="camera"),
    path("v1/reports", ReportView.as_view(), name="reports"),
    path("v1/filters/criminal_profiler/processed_images/<int:camera_api_id>/<int:image_index>",
         ImageFilterView.as_view(), name="filter_with_criminal_profiler"),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/extensions/cameras', GetCamerasView.as_view(), name='get_cameras_from_api_extension'),
]
