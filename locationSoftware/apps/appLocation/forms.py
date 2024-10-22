from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Location, Lodgement, TypeLodgement


class HouseForm(forms.ModelForm):
    class Meta:
        model = Lodgement
        fields = "__all__"


class TypeForm(forms.ModelForm):
    class Meta:
        model = TypeLodgement
        fields = "__all__"


class FormLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


class SignUpUser(UserCreationForm):
    email = forms.EmailField(required=True)  # On ajoute un champ email

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
