from apps.app_location.forms import SignUpUser
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.


# classes de la gestion des utilisateurs
class UserLoginView(LoginView):
    template_name = "appLocation/registration/sign_in_user.html"
    success_url = "{request.META.get('HTTP_REFERER', '/')}"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class RegisterView(CreateView):
    form_class = SignUpUser
    template_name = "appLocation/registration/sign_up_user.html"


# class RegisterView(View):
#     def get(self, request):
#         form = SignUpUser()
#         return render(
#             request, "appLocation/registration/sign_up_user.html", {"form": form}
#         )

#     def post(self, request):
#         form = SignUpUser(request.POST)
#         if form.is_valid():
#             form.save()
#             print("bien enregistreE")
#             return redirect("login")  # Redirection vers la page de connexion
#         return render(
#             request, "appLocation/registration/sign_up_user.html", {"form": form}
#         )
