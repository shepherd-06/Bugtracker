from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from django.http import JsonResponse
from user.serializer import UserSerializer
from uuid import uuid4


class UserRegistration(APIView):

    @staticmethod
    def post(request):
        data = request.data
        data['username'] = str(uuid4())[:12]
        serializer = UserSerializer(data=request.data)
        
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
