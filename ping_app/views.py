from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView


# Create your views here.
class Ping(APIView):
    
    def post(self, request):
        pass