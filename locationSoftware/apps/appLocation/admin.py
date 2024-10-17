from django.contrib import admin
from .models import Lodgement,Quartier,TypeLodgement

admin.site.register(Quartier)
admin.site.register(TypeLodgement)
admin.site.register(Lodgement)


