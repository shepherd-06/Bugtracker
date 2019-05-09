from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from uuid import uuid4

from bugtracker.models import User, UserToken
from bugtracker.serializer import UserTokenSerializer


class Login(APIView):

    @staticmethod
    def get_user_object(email):
        try:
            user = User.objects.get(user_email=email)
            return user
        except User.DoesNotExist:
            # Token Invalid
            return None
        except ValidationError:
            # Token Invalid
            return None

    @staticmethod
    def get_user_token(user_id):
        try:
            token_obj = UserToken.objects.get(authorized_user=user_id)
            return token_obj
        except UserToken.DoesNotExist:
            # User Token does not exist
            return None
        except ValidationError:
            # User Token does not exist
            return None

    def post(self, request):
        data = request.data
        if 'email' not in data or 'password' not in data:
            # error
            return JsonResponse({
                "message": "Email/Password field is empty!",
                "status": status.HTTP_400_BAD_REQUEST
            })

        user = self.get_user_object(data['email'])
        if user is None:
            # error
            return JsonResponse({
                "message": "Username, Password did not match!",
                "status": status.HTTP_401_UNAUTHORIZED
            })
        if check_password(data['password'], user.password):
            token_obj = self.get_user_token(user.user_id)
            if token_obj is None:
                # Create new access token
                payload = {
                    'authorized_user': user.user_id
                }
                token_serializer = UserTokenSerializer(data=payload)
                if token_serializer.is_valid():
                    token = token_serializer.save()

                    return JsonResponse({
                        "message": "success",
                        "status": status.HTTP_202_ACCEPTED,
                        "token": token.token,
                        "refresh_token": token.refresh_token,
                        "generated_at": token.generated_at,
                        "ttl": token.time_to_live
                    })
                else:
                    return JsonResponse({
                        "message": "Token Rejected",
                        "status": status.HTTP_409_CONFLICT,
                    })
            else:
                # change the previous access token
                token_obj.token = uuid4()
                token_obj.refresh_token = uuid4()
                token_obj.generated_at = timezone.now()

                token_obj.save()
                return JsonResponse({
                    "message": "success",
                    "status": status.HTTP_202_ACCEPTED,
                    "token": token_obj.token,
                    "refresh_token": token_obj.refresh_token,
                    "generated_at": token_obj.generated_at,
                    "ttl": token_obj.time_to_live
                })
        else:
            return JsonResponse({
                "message": "Username, Password did not match!",
                "status": status.HTTP_401_UNAUTHORIZED
            })

