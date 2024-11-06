from datetime import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import HouseForm, RentalForm, SignUpUser
from .models import House, Rental


class Home(TemplateView):
    template_name = "appLocation/index.html"


class ShowAllHouses(ListView):
    paginate_by = 3
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


def add_lodgement(request):
    if request.method == "POST":
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("houses")
    else:
        form = HouseForm()
    return render(request, "appLocation/add_house.html", {"form": form})


class CreateRental(LoginRequiredMixin, CreateView):
    form_class = RentalForm
    template_name = "appLocation/add_location.html"
    success_url = reverse_lazy("houses")

    def form_valid(self, form):
        house = House.objects.get(id=self.kwargs["house"])
        form.instance.user = self.request.user
        form.instance.house = house
        form.instance.date_begin = timezone.now()

        return super().form_valid(form)


# def add_location(request):
#     if request.method == "POST":
#         form = FormLocation(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("houses")
#         else:
#             form = FormLocation()
#             template_name = "appLocation/add_location.html"
#         return render(request, template_name, {"form": form})
#


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
