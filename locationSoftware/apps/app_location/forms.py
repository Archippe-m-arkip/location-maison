from apps.authuser.models import CustomUserManager, User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import House, Paid, Payment, Rental


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ["created_by", "deleted_at"]


class FormLocation(forms.ModelForm):
    class Meta:
        model = Rental
        fields = "__all__"


class SignUpUser(UserCreationForm):

    email = forms.EmailField(required=True)  # On ajoute un champ email

    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]


class Payment(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
