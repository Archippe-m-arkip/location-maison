# from django import forms
from django.db import models

from ..authuser.models import User


class House(models.Model):
    id = models.AutoField(primary_key=True)
    nbrRooms = models.IntegerField()
    type_house = models.TextField(null=True)
    quarter = models.TextField(null=False)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True)
    superficies = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="houses")

    def __int__(self):
        return self.type_house


class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    date_rent = models.DateTimeField(null=False, blank=False)
    date_begin = models.DateTimeField(null=False, blank=False)
    date_end = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter")


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_payment = models.DateTimeField(null=False)
    type_payment = models.TextField(null=True)


class Paid(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payments"
    )
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name="rented")

    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="paid_house"
    )

    def __str__(self):
        return self.house
