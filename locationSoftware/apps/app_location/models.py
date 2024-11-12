# from django import forms
from apps.authuser.models import User
from apps.core.models import BaseModel
from django.db import models
from django.db.models import Count
from django.utils import timezone


class House(BaseModel):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to="houses/", default="pas_d'image_house_selectionnee.jpg"
    )
    nbrRooms = models.IntegerField()
    type_house = models.CharField(null=True)
    quarter = models.CharField(null=False)
    address = models.TextField(max_length=255)
    description = models.TextField(null=True)
    superficies = models.FloatField()
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_available(self):
        # houses =[]
        # for rental in Rental.objects.all():
        #     houses.append(rental.house)

        # if self in houses:
        #     return False
        # return True
        # ce code ci haut est equivalent de celui-ci en terme de fonctionnement
        if self in [rental.house for rental in Rental.objects.all()]:
            return False
        return True


class Rental(BaseModel):
    id = models.AutoField(primary_key=True)
    date_rent = models.DateTimeField(null=False, blank=False, default=timezone.now())
    date_begin = models.DateTimeField(null=False, blank=False, default=timezone.now())
    date_end = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renter")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="rented")


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
