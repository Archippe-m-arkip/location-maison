from django.urls import path

from . import views
from .views import DetailsHouse, Home, ShowAllHouses, UpdateHouse

urlpatterns = [
    path("", Home.as_view(), name="home"),
    # path("les-maisons/", views.show_all_houses, name="houses"),
    path("les-maisons/", ShowAllHouses.as_view(), name="houses"),
    path("les-maisons/details/<pk>", DetailsHouse.as_view(), name="details"),
    path("les-maisons/details/<pk>/modifier", UpdateHouse.as_view(), name="update"),
    path("ajouter-maison/", views.add_lodgement, name="add_house"),
    path("ajouter-location/", views.add_location, name="add_location"),
    path("inscription/", views.signing_up, name="sign_up_user"),
    path("login/", views.signing_in, name="sign_in_user"),
]
