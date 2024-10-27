from django.contrib.auth import authenticate, login

# from django.core.signals import request_started
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import FormLocation, HouseForm, SignUpUser
from .models import House


class Home(TemplateView):
    template_name = "app_location/index.html"


class ShowAllHouses(ListView):
    model = House


class DetailsHouse(DetailView):
    model = House


class UpdateHouse(UpdateView):
    model = House
    fields = "__all__"
    success_url = ""


def add_lodgement(request):
    if request.method == "POST":
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = HouseForm()
    return render(request, "app_location/add_house.html", {"form": form})


def add_location(request):
    if request.method == "POST":
        form = FormLocation(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
        else:
            form = FormLocation()
        return render(request, "app_location/add_location.html", {"form": form})


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
    return render(
        request, "app_location/registration/sign_up_user.html", {"form": form}
    )


def signing_in(request):
    return render(request, "app_location/registration/sign_in_user.html")
