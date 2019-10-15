from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views import View
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView

from user.models import CustomUser
from user.serializer import UserSerializer
from utility.helper import get_user_object, set_cookie
from utility.token_manager import encode_access_token, encode_refresh_token


class UserRegistration(View):

    def post(self, request):
        data = {
            "email": request.POST["email"],
            "password": request.POST["password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
        }
        data['username'] = str(uuid4())[:12]
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user_registered = serializer.save()

            if user_registered:
                message = "User created successfully. Please login now"
                return HttpResponseRedirect(
                    reverse("index") +
                    "?register_message={}&status={}".format(message, True),
                )
            else:
                message = "User creation failed."
                return HttpResponseRedirect(
                    reverse("index") +
                    "?register_message={}&status={}".format(message, False),
                )
        else:
            message = "User creation failed. {}".format(serializer.errors)
            return HttpResponseRedirect(
                reverse("index") +
                "?register_message={}&status={}".format(message, False),
            )


class UserLogin(View):

    required_field = ('email', 'password')

    def post(self, request):
        data = {
            "email": request.POST["email"],
            "password": request.POST["password"],
        }
        for field in self.required_field:
            if field not in data:
                message = "Missing required field. {} is required".format(
                    field)
                return HttpResponseRedirect(
                    reverse("index") +
                    "?login_message={}&status={}".format(message, False),
                )

        user = get_user_object(email=data['email'])

        if user is None:
            # error
            message = "Username, Password did not match!"
            return HttpResponseRedirect(
                reverse("index") +
                "?login_message={}&status={}".format(message, False),
            )
        else:
            if check_password(data['password'], user.password):
                user.last_login = timezone.now()
                user.save()

                access_token = str(encode_access_token(user.username, "user"))
                refresh_token = str(
                    encode_refresh_token(user.username, "user"))

                response = HttpResponseRedirect(
                    reverse("dashboard"))
                expiry = datetime.utcnow() + timedelta(hours=5)
                set_cookie(response, "access_token",
                           access_token, expired_at=expiry)
                set_cookie(response, "refresh_token", refresh_token)
                return response
            else:
                message = "Username, Password did not match!"
                return HttpResponseRedirect(
                    reverse("index") +
                    "?login_message={}&status={}".format(message, False),
                )
