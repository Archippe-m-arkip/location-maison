from apps.app_location.models import House
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        exclude = ["deleted_at"]


class HouseDeserializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["id", "type_house", "price", "quarter", "address", "nbrRooms"]

    def create(self, validated_data):
        return House.objects.create(**validated_data)
