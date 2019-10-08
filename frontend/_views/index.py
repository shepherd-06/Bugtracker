from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.


class Index(APIView):

    def get(self, request):
        context = dict()
        if "login_message" in request.GET:
            context["login_message"] = request.GET["login_message"]

        if "register_message" in request.GET:
            context["register_message"] = request.GET["register_message"]

        if "status" in request.GET:
            context["status"] = request.GET["status"]
        return render(request, 'frontend/index.html', context)
