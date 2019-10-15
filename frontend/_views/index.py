from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from rest_framework.views import APIView

from utility.helper import get_user_object
from utility.token_manager import decode_token

# Create your views here.


class Index(APIView):

    def get(self, request):
        if request.COOKIES.get("access_token") is not None:
            payload = decode_token(request.COOKIES.get("access_token"))
            user = get_user_object(username=payload["sub"])
            
            if user is not None:
                # HTTP redirect
                return HttpResponseRedirect(reverse("dashboard"))

        context = dict()
        if "login_message" in request.GET:
            context["login_message"] = request.GET["login_message"]

        if "register_message" in request.GET:
            context["register_message"] = request.GET["register_message"]

        if "status" in request.GET:
            context["status"] = request.GET["status"]
        return render(request, 'frontend/index.html', context)
