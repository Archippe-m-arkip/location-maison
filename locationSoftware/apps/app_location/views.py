from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import FormLocation, HouseForm, SignUpUser
from .models import House, Rental


class Home(TemplateView):
    template_name = "appLocation/index.html"


class ShowAllHouses(ListView):
    model = House
    template_name = "appLocation/lodgement_list.html"

    def get_queryset(self):
        return House.objects.all()


class DetailsHouse(DetailView):
    model = House
    template_name = "appLocation/lodgement_detail.html"
    context_object_name = "theHouse"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Cette maison a été supprimée.")
        return obj


class DeleteHouse(ListView):
    def post(self, request, pk):
        house = get_object_or_404(House, pk=pk)
        house.delete()  # Suppression douce
        return redirect("houses")


class UpdateHouse(UpdateView):
    model = House
    template_name = "appLocation/lodgement_form.html"
    fields = "__all__"
    success_url = "/les-maisons/"


class UpdateRental(UpdateView):
    model = Rental
    template_name = "appLocation/rental_form.html"
    fields = "__all__"
    success_url = "/les-maisons/"


# # classes de la gestion des utilisateurs
# class UserLoginView(LoginView):
#     template_name = "appLocation/registration/sign_in_user.html"
#     success_url = reverse_lazy("home")
#
#
# class UserLogoutView(LogoutView):
#     next_page = reverse_lazy("home")
#
#
# class RegisterView(View):
#     def get(self, request):
#         form = SignUpUser()
#         return render(
#             request, "appLocation/registration/sign_up_user.html", {"form": form}
#         )
#
#     def post(self, request):
#         form = SignUpUser(request.POST)
#         if form.is_valid():
#             form.save()
#             print("bien enregistreE")
#             return redirect("login")  # Redirection vers la page de connexion
#         return render(
#             request, "appLocation/registration/sign_up_user.html", {"form": form}
#         )


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


#
# def signing_in(request):
#     return render(request, "appLocation/registration/sign_in_user.html")
