from django.contrib import admin

from ..authuser.models import User
from .models import House, Paid, Payment, Rental

admin.site.register(User)
admin.site.register(House)
admin.site.register(Rental)
admin.site.register(Payment)
admin.site.register(Paid)
