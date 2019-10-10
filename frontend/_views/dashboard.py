from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from projects.models import Projects
from team.models import Team
from ping_app.models import WebStatus
from utility.helper import get_common_view_payload, get_user_object, set_cookie
from utility.token_manager import decode_token, protected

# Create your views here.


class DashboardView(View):

    HTTP_Methods = {
        "1": "Get",
        "2": "Head",
        "3": "Options",
    }

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        context = get_common_view_payload(user, "Dashboard")
        if "ping_message" in request.GET:
            context["ping_message"] = request.GET["ping_message"]
        if "status" in request.GET:
            context["status"] = False
        else:
            context["status"] = True

        web_status = WebStatus.objects.all()
        server_payload = list()
        counter = 1
        for web in web_status:
            server_payload.append({
                "index": counter,
                "url": web.url,
                "last_checked": web.last_checked,
                "status": web.status,
                "request_type": self.HTTP_Methods[web.request_type],
            })
            counter += 1
        context["server_status"] = server_payload
        context["methods"] = [
            {
                "id": 1,
                "type": "Get",
            },
            {
                "id": 2,
                "type": "Head",
            },
            {
                "id": 3,
                "type": "Options",
            }
        ]
        response = render(request, 'frontend/dashboard.html', context)
        return response
