from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from connectivity.models import CameraCluster


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class ImagePlayerSerializer(serializers.Serializer):
    images = Base64ImageField(many=True)


class LocationSerializer(serializers.Serializer):
    country = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField()
    street = serializers.CharField()


class CameraSerializer(serializers.Serializer):
    webcam_id = serializers.IntegerField()
    status = serializers.CharField()
    categories = CategorySerializer(many=True)
    location = LocationSerializer(required=False)
    player = ImagePlayerSerializer(required=False)


class ClusterMetaSerializer(serializers):
    class Meta:
        model = CameraCluster
        fields = '__all__'


class CameraClusterSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True)
    cluster_meta = ClusterMetaSerializer()
