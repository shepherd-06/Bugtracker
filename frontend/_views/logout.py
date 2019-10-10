from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from utility.token_manager import decode_token, protected
from utility.helper import get_user_object


class LogoutView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        response = HttpResponseRedirect(reverse('index'))
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        response.delete_cookie('olfsk')
        response.delete_cookie('hblid')
        return response
