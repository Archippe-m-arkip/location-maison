from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class CheckUserAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        links = ["/mes-reservations/", "/ajouter-maison/"]
        for link in links:
            print(link)
            if request.path.startswith(link) and not request.user.is_authenticated:
                return redirect("login")
        response = self.get_response(request)
        return response
