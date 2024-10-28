from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

# from django.core.signals import request_started
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import FormLocation, HouseForm, SignUpUser
from .models import House


class Home(TemplateView):
    template_name = "appLocation/index.html"


class ShowAllHouses(ListView):
    model = House
    template_name = "appLocation/lodgement_list.html"


class DetailsHouse(DetailView):
    model = House
    template_name = "appLocation/lodgement_detail.html"
    house = House()
    context_object_name = "theHouse"


class UpdateHouse(UpdateView):
    model = House
    fields = "__all__"
    success_url = ""


class UserLogin(LoginView):
    template_name = "registration/sign_in_user.html"
    success_url = reverse_lazy("home")


def add_lodgement(request):
    if request.method == "POST":
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = HouseForm()
    return render(request, "appLocation/add_house.html", {"form": form})


def add_location(request):
    if request.method == "POST":
        form = FormLocation(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
        else:
            form = FormLocation()
            template_name = "appLocation/add_location.html"
        return render(request, template_name, {"form": form})


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
