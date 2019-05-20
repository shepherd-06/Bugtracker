import uuid

from django.http import JsonResponse
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
        try:
            if token_obj.token != uuid.UUID(data['token'])\
                    or token_obj.refresh_token != uuid.UUID(data['refresh_token']):
                return JsonResponse({
                    "message": "Invalid Token/Refresh Token!",
                    "status": status.HTTP_401_UNAUTHORIZED
                })
        except ValueError:
            return JsonResponse({
                "message": "Token malformed!",
                "status": status.HTTP_401_UNAUTHORIZED
            })
        token_obj.save()
        if token_obj.pk:
            return JsonResponse({
                "message": "success",
                "status": status.HTTP_202_ACCEPTED  ,
                "user_id": data['user_id'],
                "token": token_obj.token,
                "refresh_token": token_obj.refresh_token,
                "generated_at": token_obj.generated_at,
                "ttl": token_obj.time_to_live
            })
        else:
            return JsonResponse({
                "message": "Token Rejected",
                "status": status.HTTP_409_CONFLICT,
            })
