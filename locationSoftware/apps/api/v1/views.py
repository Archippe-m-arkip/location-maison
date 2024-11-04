from apps.app_location.models import House
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

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


#


class HouseListView_v1(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
