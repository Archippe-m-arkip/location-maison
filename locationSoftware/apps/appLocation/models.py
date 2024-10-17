from django.db import models
from django import forms




class TypeLodgement(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.type



class Quartier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Lodgement(models.Model):
    id = models.AutoField(primary_key=True)
    description =models.TextField(null=True)
    nbrRooms = models.IntegerField()
    superficies = models.FloatField()
    address =models.CharField(max_length=150)
    type_lodgement = models.ForeignKey(TypeLodgement, on_delete=models.CASCADE, related_name='lodgements')
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='lodgements')

    def __int__(self):
        return self.nbrRooms


class Locator(models.Model):
    id = models.AutoField(primary_key=True)
    name =models.CharField(max_length=50, null=False, blank=False)
    phone =models.IntegerField(null=False, blank=False)
    email =models.EmailField()
    password =models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    id= models.AutoField(primary_key=True)
    date_begin = models.DateTimeField(null=False, blank=False)
    date_end = models.DateTimeField(null=False, blank=False)
    lodgement =models.ForeignKey(Lodgement,on_delete=models.CASCADE,related_name='locations_lodg')
    locator = models.ForeignKey(Locator, on_delete=models.CASCADE, related_name='locations_loc')

    def __str__(self):
        return self.date_end
