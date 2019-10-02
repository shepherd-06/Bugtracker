from uuid import uuid4

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import CustomUser
from user.serializer import UserSerializer
from utility.helper import get_user_object
from django.views import View


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
            email = serializer.validated_data['email']
            user_registered = serializer.save()

            if user_registered:
                return JsonResponse({
                    "message": "User created successfully",
                    "email": email,
                    "status": HTTP_201_CREATED
                })
            else:
                return JsonResponse({
                    "message": "User creation failed.",
                    "status": HTTP_406_NOT_ACCEPTABLE
                })
        else:
            return JsonResponse({
                "message": "User creation failed. {}".format(serializer.errors),
                "status": HTTP_400_BAD_REQUEST
            })


class UserLogin(APIView):

    required_field = ('email', 'password')

    def post(self, request):
        data = request.data
        for field in self.required_field:
            if field not in data:
                return JsonResponse({
                    "message": "Missing required field. {} is required".format(field),
                    "status": False,
                    "status_code": HTTP_400_BAD_REQUEST,
                })

        user = get_user_object(email=data['email'])

        if user is None:
            # error
            return JsonResponse({
                "message": "Username, Password did not match!",
                "status": False,
                "status_code": HTTP_401_UNAUTHORIZED,
            }, status=HTTP_401_UNAUTHORIZED)
        else:
            if check_password(data['password'], user.password):
                refresh = RefreshToken.for_user(user)
                user.last_login = timezone.now()
                user.save()

                return JsonResponse({
                    "message": "success",
                    "status": True,
                    "username": user.username,
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    "status_code": HTTP_202_ACCEPTED,
                    "is_verified": user.pin_verified,
                    "is_staff": user.is_staff,
                }, status=HTTP_202_ACCEPTED)
            else:
                return JsonResponse({
                    "message": "Username, Password did not match!",
                    "status": False,
                    "status_code": HTTP_401_UNAUTHORIZED,
                }, status=HTTP_401_UNAUTHORIZED)
