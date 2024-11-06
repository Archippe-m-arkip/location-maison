from apps.app_location.models import House, Rental


def rent_context(request):
    rent = Rental.objects.all()
    return {"rent": rent}
