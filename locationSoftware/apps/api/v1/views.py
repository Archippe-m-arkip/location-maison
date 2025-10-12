from crypt import methods

from apps.app_location.models import House, Rental
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.parsers import JSONParser
from .permissions import IsOwnerOrReadOnly
from yaml import serialize

from .serializers import HouseDeserializer, HouseSerializer, RentalSerializer




class HouseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type_house', 'quarter']
    search_fields = ['type_house', 'quarter', 'price']

    @action(detail=False, methods=['get'])
    def available(self,request):
        house_available = self.queryset.filter(availability=True)
        serializer = self.get_serializer(house_available, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

