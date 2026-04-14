from apps.app_location.models import House
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .serializers import HouseDeserializer, HouseSerializer


@csrf_exempt
def create_house(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = HouseDeserializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)


class HouseListView_v2(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    def get_queryset(self):
        return House.objects.filter(type_house="appart")
