from apps.app_location.models import House
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers import HouseDeserializer, HouseSerializer

house_data = House.objects.all()
serializer = HouseSerializer(house_data, many=True)
serializer_data = JSONRenderer().render(serializer.data)
print(serializer_data)


@csrf_exempt
def create_house(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = HouseDeserializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


# APIView est bcp plus flexible et n'est utiliseE que lorsqu'on a besoin de definir ses propres codes
# Dans la maniere de gerer les requetes. get, post, put patch
class HouseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        houses = House.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = HouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class HouseListView(generics.ListCreateAPIView):
#     queryset = House.objects.all()
#     serializer_class = HouseSerializer
