from django.shortcuts import render
from django.views import View

class HowItWorks(View):
    
    def get(self, request):
        return render(request, 'frontend/how_it_works.html')