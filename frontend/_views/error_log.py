from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from utility.token_manager import protected, decode_token
from utility.helper import get_user_object, get_common_view_payload


class ErrorLogView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        context = get_common_view_payload(user, "Error Log")
        return render(request, 'frontend/error_log.html', context)
