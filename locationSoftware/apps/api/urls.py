from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets

from ..api.views import HouseListView

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("maisons", HouseListView.as_view()),
]
