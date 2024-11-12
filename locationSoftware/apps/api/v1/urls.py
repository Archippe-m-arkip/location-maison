from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import HouseListView_v1

app_name = "api"

urlpatterns = [
    path("les-maisons", HouseListView_v1.as_view()),
    path("connexion", obtain_auth_token, name="login"),
]
