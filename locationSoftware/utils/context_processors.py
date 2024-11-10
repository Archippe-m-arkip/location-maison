from apps.app_location.models import House, Rental
from django.utils import timezone


def rent_context(request):

    not_available_houses = House.objects.filter(availability=False)
    rents = Rental.objects.all()
    for rent in rents:
        for not_available in not_available_houses:
            if rent.house == not_available:
                return {
                    "rent": rent,
                    "rents": rents,
                }


def remaining_time_context(request):
    not_available_houses = House.objects.filter(availability=False)
    rents = Rental.objects.all()
    for rent in rents:
        remaining_time = timezone.now() - rent.date_end
        for not_available in not_available_houses:
            if rent.house == not_available:
                if remaining_time > 0:
                    remaining_time = remaining_time + "pour expirer"

                elif remaining_time == 0:
                    remaining_time = "expire aujourd'hui"

                else:
                    remaining_time = remaining_time + "apres expiration"
                    print(remaining_time)
            return {"remaining_time": remaining_time}


def rents_order_by_date_end(request):
    rents = Rental.objects.all().order_by("-date_end")
    return {"rents_by_date_end": rents}
