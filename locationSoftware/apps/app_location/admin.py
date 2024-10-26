from django.contrib import admin

from ..authuser.models import User
from .models import Lodgement, Quartier, TypeLodgement

admin.site.register(Quartier)
admin.site.register(TypeLodgement)
admin.site.register(Lodgement)
admin.site.register(User)
