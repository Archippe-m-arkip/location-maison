from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home' ),
    path('les-maisons/', views.show_all_houses, name='houses'),
    path('les-maisons/details/<int:id>', views.detail_house, name='details'),

    path('ajouter-maison/', views.add_lodgement, name='add_house'),
    path('ajouter-type/', views.add_type_house, name='add_type_house'),
    path('ajouter-location/', views.add_location, name='add_location'),

    path('inscription/', views.signing_up, name='sign_up_user'),
    path('login/', views.signing_in, name='sign_in_user'),

]
