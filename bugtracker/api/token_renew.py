from uuid import uuid4

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.utility import get_user_token, get_user_object


class UserTokenRenew(APIView):

    def post(self, request):
        """
        this function will renew user token. Remove the previous token and create a brand new entry
        Required in request:
        ***user_id, current_token, refresh_token***
        :param request: Django post request
        :return: new token
        """
        data = request.data
        if 'user_id' not in data or 'token' not in data or 'refresh_token' not in data:
            # Error - missing parameter
            return JsonResponse({
                "message": "Missing parameters! User_id, token and refresh_token is required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        token_obj = get_user_token(get_user_object(data['user_id']))
        if token_obj is None:
            return JsonResponse({
                "message": "Invalid User!",
                "status": status.HTTP_401_UNAUTHORIZED
            })

        if token_obj.token != data['token'] or token_obj.refresh_token != data['refresh_token']:
            return JsonResponse({
                "message": "Invalid Token/Refresh Token!",
                "status": status.HTTP_401_UNAUTHORIZED
            })

        token_obj.token = uuid4()
        token_obj.refresh_token = uuid4()
        token_obj.generated_at = timezone.now()
        update_status = token_obj.save()

        print(update_status)
        return JsonResponse({
            "status": status.HTTP_200_OK
        })
