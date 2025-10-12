from apps.app_location.models import House, Rental
from .serializers import HouseDeserializer, HouseSerializer, RentalSerializer
from rest_framework import viewsets



class HouseViewSet(viewsets.ModelViewSet):
    queryset =  House.objects.all()
    serializer_class = HouseSerializer


