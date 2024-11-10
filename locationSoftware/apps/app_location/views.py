from calendar import month
from pydoc import resolve

from apps.authuser.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from urllib3 import request

from .forms import HouseForm, RentalForm, SignUpUser
from .models import House, Rental


class Home(TemplateView):
    template_name = "appLocation/index.html"


class ShowAllHouses(ListView):
    paginate_by = 3
    model = House
    template_name = "appLocation/lodgement_list.html"

    def get_queryset(self):
        available = self.request.GET
        print(available)
        if available:
            available = self.request.GET.get("disponible")

            if available == "true":
                object_list = House.objects.all().exclude(availability=False)
                return object_list

            elif available == "false":
                object_list = House.objects.filter(availability=False)
                return object_list

            elif available == "all":
                object_list = House.objects.all()
                return object_list

            elif available == "soon":
                not_available_houses = House.objects.filter(availability=False)
                # today = timezone.now()
                rent_object = Rental.objects.all().order_by("-date_end")

                for rental in rent_object:
                    for not_available in not_available_houses:
                        if rental.house == not_available:
                            obj_list = rent_object

                return not_available_houses
        else:
            print("Noooooooone")
            object_list = House.objects.all()

            return object_list

        object_list = House.objects.all()
        return object_list


class Activities(ListView):
    model = House
    template_name = "appLocation/activities.html"

    def get_queryset(self):
        object_list = House.objects.all()
        return object_list


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
    fields = [
        "created_by",
        "type_house",
        "nbrRooms",
        "image",
        "quarter",
        "superficies",
        "address",
        "description",
        "user",
    ]
    success_url = "/les-maisons/"


class UpdateRental(UpdateView):
    model = Rental
    template_name = "appLocation/rental_form.html"
    fields = "__all__"
    success_url = "/les-maisons/"


def add_lodgement(request):
    if request.method == "POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = HouseForm()
    return render(request, "appLocation/add_house.html", {"form": form})


class CreateRental(CreateView):
    model = Rental
    form_class = RentalForm
    template_name = "appLocation/add_location.html"
    success_url = reverse_lazy("houses")

    def get_initial(self):
        house_id = self.kwargs.get("house_id")
        user_id = self.kwargs.get("user_id")
        house = get_object_or_404(House, id=house_id)
        user = get_object_or_404(User, id=user_id)
        return {
            "house": house,
            "user": user,
            "username_locator": self.request.user.username,
        }

    def form_valid(self, form):
        house_id = self.kwargs.get("house_id")
        house = get_object_or_404(House, id=house_id)
        house.availability = False
        house.save()
        rental = RentalForm()
        if rental.is_valid():
            rental.save()
        else:
            print(rental.errors)
        return super().form_valid(form)


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


# def signing_in(request):
#     return render(request, "appLocation/registration/sign_in_user.html")
