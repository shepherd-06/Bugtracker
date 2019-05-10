from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.model_managers.models import UserToken
from bugtracker.utility import token_invalid


class Logout(APIView):

    @staticmethod
    def user_token_validity(user_token):
        try:
            user_token = UserToken.objects.get(token=user_token)
            return user_token
        except UserToken.DoesNotExist:
            return -1
        except ValidationError:
            return -1

    def get(self, request):
        token = request.GET.get('token')
        if token is None:
            return JsonResponse(token_invalid)

        token_obj = self.user_token_validity(token)
        if token_obj != -1:
            state = UserToken.objects.filter(token=token).delete()
            if state:
                return JsonResponse({
                    "message": "Logout",
                    "status": status.HTTP_200_OK
                })
            else:
                return JsonResponse({
                    "message": "Error Occurred!",
                    "status": status.HTTP_400_BAD_REQUEST
                })
        else:
            return JsonResponse({
                "message": "Error Occurred!",
                "status": status.HTTP_400_BAD_REQUEST
            })
