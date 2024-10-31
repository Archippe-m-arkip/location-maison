from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import (
    DeleteHouse,
    DetailsHouse,
    Home,
    RegisterView,
    ShowAllHouses,
    UpdateHouse,
    UserLogoutView,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    # path("les-maisons/", views.show_all_houses, name="houses"),
    path("les-maisons/", ShowAllHouses.as_view(), name="houses"),
    path("les-maisons/details/<pk>", DetailsHouse.as_view(), name="details"),
    path("les-maisons/modifier/<pk>", UpdateHouse.as_view(), name="update"),
    path("les-maisons/supprimer/<pk>", DeleteHouse.as_view(), name="delete"),
    path("ajouter-maison/", views.add_lodgement, name="add_house"),
    path("ajouter-location/", views.add_location, name="add_location"),
    path("inscription/", RegisterView.as_view(), name="sign_up_user"),
    path(
        "connexion/",
        obtain_auth_token,
        name="login",
    ),
    path("deconnexion/", UserLogoutView.as_view(), name="logout"),
]
