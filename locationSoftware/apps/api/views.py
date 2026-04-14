from apps.app_location.models import House, Rental
from rest_framework import viewsets

from .serializers import HouseDeserializer, HouseSerializer, RentalSerializer


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
