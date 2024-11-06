from apps.authuser.views import RegisterView, UserLoginView, UserLogoutView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import (
    CreateRental,
    DeleteHouse,
    DetailsHouse,
    Home,
    ShowAllHouses,
    UpdateHouse,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    # path("les-maisons/", views.show_all_houses, name="houses"),
    path("les-maisons/", ShowAllHouses.as_view(), name="houses"),
    path("les-maisons/details/<pk>", DetailsHouse.as_view(), name="details"),
    path("les-maisons/modifier/<pk>", UpdateHouse.as_view(), name="update"),
    path("les-maisons/supprimer/<pk>", DeleteHouse.as_view(), name="delete"),
    path("ajouter-maison/", views.add_lodgement, name="add_house"),
    path("ajouter-location/", CreateRental.as_view(), name="add_location"),
    path("inscription/", RegisterView.as_view(), name="sign_up_user"),
    path(
        "connexion/",
        UserLoginView.as_view(),
        name="login",
    ),
    path("deconnexion/", UserLogoutView.as_view(), name="logout"),
]
