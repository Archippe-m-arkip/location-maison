from apps.app_location.models import House, Rental
from django.contrib.auth.models import Group, User
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        exclude = ["deleted_at"]


class HouseDeserializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"

    def create(self, validated_data):
        return House.objects.create(**validated_data)


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"
