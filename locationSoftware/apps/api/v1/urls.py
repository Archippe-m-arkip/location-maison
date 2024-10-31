from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urls import app_name

from .views import HouseListView_v1

app_name = "api"

urlpatterns = [
    path("maisons", HouseListView_v1.as_view()),
    path("login", obtain_auth_token, name="login"),
]
