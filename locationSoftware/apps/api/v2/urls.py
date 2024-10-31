from django.urls import path

from .views import HouseListView_v2

urlpatterns = [path("maisons/", HouseListView_v2.as_view())]
