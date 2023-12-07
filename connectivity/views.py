from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DistrictListSerializer
from .models import District, CameraCluster, Camera


class DistrictListView(APIView):

    def get(self, request, city: str):
        districts = District.objects.filter(city__name__iexact=city)
        districts_data = {'districts': []}
        if bool(districts):
            for district in districts:
                camera_cluster = CameraCluster.objects.get(district=district)
                cameras_count = Camera.objects.filter(camera_cluster=camera_cluster).count()
                districts_data['districts'].append({
                    'id': district.id,
                    'name': district.name,
                    'cameras_count': cameras_count
                })
        serializer = DistrictListSerializer(data=districts_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
