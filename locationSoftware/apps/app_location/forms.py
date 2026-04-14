from apps.authuser.models import CustomUserManager, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from .models import House, Paid, Payment, Rental


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ["created_by", "deleted_at"]


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ["house", "user", "date_begin", "date_end"]


class SignUpUser(UserCreationForm):
    email = forms.EmailField(required=True)  # On ajoute un champ email
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["name", "username", "image", "email", "password1", "password2"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
