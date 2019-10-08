from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from projects.models import Projects
from team.models import Team
from utility.helper import get_common_view_payload, get_user_object, set_cookie
from utility.token_manager import decode_token, protected

# Create your views here.


class DashboardView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        context = get_common_view_payload(user, "Dashboard")
        response = render(request, 'frontend/dashboard.html', context)
        return response
