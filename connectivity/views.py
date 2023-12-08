from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DistrictListSerializer, CameraClusterSerializer, ClusterMetaSerializer, ClusterWithLocationSerializer
from .models import District, CameraCluster, Camera, Country, City, Street
from logging import getLogger
from services.connectivity import WindyApi, WindyDataManager
from custom_exceptions.windy_api import NoSuchCameraException, ResponseException


logger = getLogger()


class DistrictListView(APIView):

    def get(self, request, city: str):
        districts = District.objects.filter(city__name__iexact=city)
        districts_data = {'districts': []}
        if bool(districts):
            for district in districts:
                try:
                    camera_cluster = CameraCluster.objects.get(district=district)
                except CameraCluster.DoesNotExist:
                    break
                cameras_count = Camera.objects.filter(camera_cluster=camera_cluster).count()
                district_data = {
                    'id': district.id,
                    'name': district.name,
                    'cameras_count': cameras_count,
                }
                include_cluster_meta = self.request.query_params.get('include')
                if include_cluster_meta == "cluster_meta":
                    try:
                        cluster = CameraCluster.objects.get(district=district)
                        district_data["cluster_meta"] = {
                            "id": cluster.id,
                            "name": cluster.name
                        }
                    except CameraCluster.DoesNotExist:
                        district_data["cluster_meta"] = None

                districts_data['districts'].append(district_data)

        serializer = DistrictListSerializer(data=districts_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ClusterView(APIView):
    def get(self, request, id:str = None, camera_cluster_name: str = None):
        if bool(id) is bool(camera_cluster_name):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data_dict = {'cameras': [], 'cluster_meta': None}
        try:
            if camera_cluster_name:
                camera_cluster = CameraCluster.objects.get(name__iexact=camera_cluster_name)
            else:
                camera_cluster = CameraCluster.objects.get(id=id)
        except CameraCluster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        camera_cluster_serializer = ClusterMetaSerializer(camera_cluster)
        data_dict.update({'cluster_meta': camera_cluster_serializer.data})
        cameras = Camera.objects.filter(camera_cluster=camera_cluster)
        cameras_list = data_dict.get('cameras')
        windy_api = WindyApi()
        for camera in cameras:
            try:
                cam_scheme = windy_api.get_camera(camera.camera_id)
            except NoSuchCameraException as e:
                logger.exception(e.message)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ResponseException as e:
                logger.exception(e.message)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            camera_dict = dict()
            camera_dict.update({
                'webcam_id': cam_scheme['webcamId'],
                'status': cam_scheme['status'],
                'categories': [{"id": category["id"], "name": category["name"]} for category in cam_scheme['categories']],
                })
            # getting location
            district = camera_cluster.district
            city = district.city
            country = city.country
            camera_dict.update(
                {
                    "location": {
                        "country": country.name,
                        "city": city.name,
                        "district": district.name
                    }
                }
            )
            cameras_list.append(camera_dict)
        serializer = CameraClusterSerializer(data=data_dict)
        return Response(data=serializer.initial_data)


class ListClustersWithLocationView(APIView):

    def get(self, request):
        clusters = CameraCluster.objects.values('id', 'name', 'district__name', 'district__city__name',
                                                'district__city__country__name')

        clusters_formatted = []
        for cluster in clusters:
            clusters_formatted.append({
                "cluster_meta": {
                    "id": cluster['id'],
                    "name": cluster['name']},
                "location": {
                    "country": cluster['district__city__country__name'],
                    "city": cluster['district__city__name'],
                    "district": cluster['district__name']
                },
            })
        serializer = ClusterWithLocationSerializer(data=clusters_formatted, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
