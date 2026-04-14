from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework.urls import app_name

# app_name = 'api'

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("v1/", include("apps.api.v1.urls")),
    path("v2/", include("apps.api.v2.urls")),
]
