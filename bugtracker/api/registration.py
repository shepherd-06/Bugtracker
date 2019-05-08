from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.serializer import UserRegistrationSerializer


class UserRegistration(APIView):

    @staticmethod
    def post(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['user_email']
            user_registered = serializer.save()

            if user_registered:
                return JsonResponse({
                    "message": "User created successfully",
                    "email": email,
                    "status": status.HTTP_201_CREATED
                })
            else:
                return JsonResponse({
                    "message": "User creation failed.",
                    "status": status.HTTP_406_NOT_ACCEPTABLE
                })
        else:
            return JsonResponse({
                "message": "User creation failed. {}".format(serializer.errors),
                "status": status.HTTP_400_BAD_REQUEST
            })
