from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import HouseViewSet, RentalViewSet

router = DefaultRouter()
house =router.register(r'maisons', HouseViewSet, basename="list_house")
rental =router.register(r'locations', RentalViewSet, basename="list_rental")


urlpatterns = [
    path("", include(router.urls)),
    path("connexion/", obtain_auth_token, name="login"),
]

