from calendar import month
from pydoc import resolve

from apps.authuser.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Min
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone, translation
from django.views.generic import CreateView, DeleteView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from urllib3 import request

from .forms import HouseForm, PaymentForm, RentalForm, SignUpUser
from .models import House, Payment, Rental


class Home(TemplateView):
    template_name = "appLocation/index.html"


class ShowAllHouses(ListView):
    paginate_by = 3
    model = House
    template_name = "appLocation/lodgement_list.html"

    def get_queryset(self):
        available = self.request.GET
        if available:
            available = self.request.GET.get("disponible")
            if available == "true":
                object_list = (
                    House.objects.select_related("user")
                    .annotate(
                        nbr_rent=Count("rented"), last_date=Max("rented__date_end")
                    )
                    .exclude(availability=False)
                )
                return object_list

            elif available == "false":
                object_list = House.objects.filter(availability=False).annotate(
                    nbr_rent=Count("rented"), last_date=Max("rented__date_end")
                )
                return object_list

            elif available == "all":
                object_list = House.objects.all().annotate(
                    nbr_rent=Count("rented"), last_date=Max("rented__date_end")
                )
                return object_list

            elif available == "soon":
                not_available_houses = (
                    House.objects.filter(availability=False)
                    .annotate(
                        nbr_rent=Count("rented"), last_date=Max("rented__date_end")
                    )
                    .order_by("last_date")
                )
                return not_available_houses
        else:
            object_list = House.objects.all().annotate(
                nbr_rent=Count("rented"), last_date=Max("rented__date_end")
            )
            return object_list

        object_list = House.objects.annotate(
            nbr_rent=Count("rented"), last_date=Max("rented__date_end")
        )
        return object_list


class MyHouses(ListView):
    paginate_by = 3
    model = House
    template_name = "appLocation/my-reservations.html"

    def get_queryset(self):
        user_id = self.request.user.id
        rental = Rental.objects.select_related("house").filter(user_id=user_id)
        return rental


class Activities(ListView):
    paginate_by = 9
    model = House
    template_name = "appLocation/activities.html"
    context_object_name = "maisons"

    def get_queryset(self):
        houses = House.objects.annotate(number_locations=Count("rented"))
        return houses


class DetailsHouse(DetailView):
    model = House
    template_name = "appLocation/lodgement_detail.html"
    context_object_name = "theHouse"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Cette maison a été supprimée.")
        return obj

    def get_queryset(self):
        return House.objects.annotate(
            nbr_locations=Count("rented"), last_date=Max("rented__date_end")
        )


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


class CreatePayment(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "appLocation/add_payement.html"
    exclude = ["user", "created_by"]
    success_url = reverse_lazy("houses")

    def get_initial(self):
        user_id = self.kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        time = timezone.now()

        return {
            "user": user,
            "time": time,
        }

    def form_valid(self, form):
        time = timezone.now()
        payment = PaymentForm()
        if payment.is_valid():
            payment.save()
        else:
            print(f"{payment.errors}")
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


def change_language(request):
    if request.method == "POST":
        lang_code = request.POST.get("language")
        translation.activate(lang_code)
        # request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
        print(f"{lang_code}--------------------------------------")
        return HttpResponse(f"Langue changee vers {request.path}")


# def signing_in(request):
#     return render(request, "appLocation/registration/sign_in_user.html")
