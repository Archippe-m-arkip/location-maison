# from django import forms
from apps.authuser.models import User
from apps.core.models import BaseModel
from django.db import models


class House(BaseModel):
    id = models.AutoField(primary_key=True)
    # image = models.ImageField(null=True)
    nbrRooms = models.IntegerField()
    type_house = models.CharField(null=True)
    quarter = models.CharField(null=False)
    address = models.TextField(max_length=255)
    description = models.TextField(null=True)
    superficies = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rental(BaseModel):
    id = models.AutoField(primary_key=True)
    date_rent = models.DateTimeField(null=False, blank=False)
    date_begin = models.DateTimeField(null=False, blank=False)
    date_end = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter")


class Payment(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_payment = models.DateTimeField(null=False)
    type_payment = models.TextField(null=True)


class Paid(BaseModel):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payments"
    )
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name="rented")

    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="paid_house"
    )
