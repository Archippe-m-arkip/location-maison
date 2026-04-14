from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import HouseListView_v2

app_name = "api"

urlpatterns = [
    path("les-maisons", HouseListView_v2.as_view()),
    path("connexion", obtain_auth_token, name="login"),
]
