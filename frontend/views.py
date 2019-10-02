from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class Index(APIView):
    
    def get(self, request):
        return render(request, 'frontend/index.html')