from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from connectivity.models import CameraCluster


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class ImagePlayerSerializer(serializers.Serializer):
    images = serializers.ListField(child=Base64ImageField())


class LocationSerializer(serializers.Serializer):
    country = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField()
    street = serializers.CharField(required=False)


class CameraSerializer(serializers.Serializer):
    webcam_id = serializers.IntegerField()
    status = serializers.CharField()
    categories = CategorySerializer(many=True)
    location = LocationSerializer(required=False)
    player = ImagePlayerSerializer(required=False)


class ClusterMetaSerializer(serializers.ModelSerializer):
    district_name = serializers.SerializerMethodField()

    def get_district_name(self, obj):
        return obj.district.name

    class Meta:
        model = CameraCluster
        fields = '__all__'


class CameraClusterSerializer(serializers.Serializer):
    cameras = CameraSerializer(many=True)
    cluster_meta = ClusterMetaSerializer()


class ClusterNotVerboseForDistrict(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cluster_meta = ClusterNotVerboseForDistrict(required=False)
    cameras_count = serializers.IntegerField(required=False)


class DistrictListSerializer(serializers.Serializer):
    districts = DistrictSerializer(many=True)
