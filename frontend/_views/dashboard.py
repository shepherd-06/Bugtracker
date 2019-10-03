from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from utility.token_manager import decode_token, protected
from utility.helper import get_user_object
# Create your views here.


class Dashboard(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        
        context = {
            "full_name": user.get_full_name
        }
        return render(request, 'frontend/dashboard.html', context)
