from apps.app_location.models import House, Rental
from django.db.models import Count
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
                    return {"remaining_time": remaining_time}

                elif remaining_time == 0:
                    return {"remaining_time": remaining_time}

                else:
                    remaining_time = remaining_time + "apres expiration"
                    print(remaining_time)
            return {"remaining_time": remaining_time}


def rented_times_number(request):
    house_rents = House.objects.annotate(nbr_rent=Count("rented"))

    for house_rent in house_rents:
        print(house_rent.nbr_rent, house_rent)
        return {"rent_times": house_rent.nbr_rent}
