from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from utility.helper import get_user_object, get_common_view_payload
from utility.token_manager import decode_token, protected


class PingView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        context = get_common_view_payload(user, user.get_full_name)
        return render(request, 'frontend/profile.html', context)
