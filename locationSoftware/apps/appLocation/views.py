from django.contrib.auth import authenticate, login
# from django.core.signals import request_started
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .forms import FormLocation, HouseForm, SignUpUser, TypeForm
from .models import Lodgement


# def home(request):
#     return render(request,'appLocation/index.html')
class Home(TemplateView):
    template_name = "appLocation/index.html"


def show_all_houses(request):
    houses = Lodgement.objects.all().values()
    return render(request, "appLocation/all_houses.html", {"houses": houses})


# class AllHouses(Lodgement):
#     houses = Lodgement.objects.all()
#     template_name = "application/all_houses.html"


def detail_house(request, id):
    # house = Lodgement.objects.get(id=id)
    house = get_object_or_404(Lodgement, id=id)
    return render(request, "appLocation/detail_house.html", {"theHouse": house})


def add_lodgement(request):
    if request.method == "POST":
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = HouseForm()
    return render(request, "appLocation/add_house.html", {"form": form})


def add_type_house(request):
    if request.method == "POST":
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = TypeForm()
    return render(request, "appLocation/add_type_house.html", {"form": form})


def add_location(request):
    if request.method == "POST":
        form = FormLocation(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
        else:
            form = FormLocation()
        return render(request, "appLocation/add_location.html", {"form": form})


def signing_up(request):
    if request.method == "POST":
        form = SignUpUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("houses")  # Redirection après inscription
    else:
        form = SignUpUser()
    return render(request, "appLocation/registration/sign_up_user.html", {"form": form})


def signing_in(request):
    return render(request, "appLocation/registration/sign_in_user.html")


#
# def reservation(request,id):
#         location = Lodgement.objects.get(id=id)
#
#         return render(request, 'appLocation/detail_house.html', {'theHouse': house})
