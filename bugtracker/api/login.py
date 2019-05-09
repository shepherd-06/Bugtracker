from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.models import User, UserToken


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
        if 'email' not in data:
            # error
            pass

        user = self.get_user_object(data['email'])
        if user is None:
            # error
            pass
        if check_password(data['password'], user.password):
            token_obj = self.get_user_token(user.user_id)
            if token_obj is None:
                # Create new access token
                pass
            else:
                # change the previous access token
                pass
            return JsonResponse({
                "hello": "world"
            })
        else:
            return JsonResponse({
                "status": status.HTTP_401_UNAUTHORIZED
            })

