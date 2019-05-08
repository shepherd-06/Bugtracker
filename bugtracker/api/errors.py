from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect

from bugtracker.utility import *
from zathura_bugtracker.custom_auth import TokenAuth


class Error(TokenAuth):

    def post(self, request):
        token = request.POST["token"]
        print("Token: {}".format(token))
        if token is None:
            return JsonResponse(token_invalid)
        status = super().token_validate(token)
        if status == -1:
            return JsonResponse(token_invalid)
        elif status == 1:
            return JsonResponse(token_expired)
        else:
            # This part is valid actually. It must not return Invalid status.
            # This part is for testing right now.
            return JsonResponse({
                'status': 200
            })

    def put(self, request):
        pass

    def get(self, request):
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        status = super().token_validate(token)
        if status == -1:
            return JsonResponse(token_invalid)
        elif status == 1:
            return JsonResponse(token_expired)
        else:
            # This part is valid actually. It must not return Invalid status.
            # This part is for testing right now.
            return JsonResponse({
                'status': 200
            })
