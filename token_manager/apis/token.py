from uuid import uuid4

from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView
from utility.token_manager import protected, decode_token

from token_manager.serializer import TokenSerializer
from utility.helper import get_user_object, get_project_object, get_project_token_by_project_id
from uuid import uuid4


class ProjectToken(View):

    @protected
    def post(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        # TODO: check if user is an admin to create a project under this org.

        if "project_id" not in request.POST:
            return JsonResponse({
                "message": "Missing required parameter. {project_id} is required",
                "status": False,
            }, status=HTTP_400_BAD_REQUEST)
        
        data = {
            "project_id": request.POST["project_id"],
        }

        project_obj = get_project_object(project_id=data["project_id"])
        if project_obj is None:
            return JsonResponse({
                "message": "Selected project not found",
                "status": False,
            }, status=HTTP_400_BAD_REQUEST)

        project_token_obj = get_project_token_by_project_id(project_obj.pk)
        if project_token_obj is not None:
            return JsonResponse({
                "message": "Token already generated for this project. One token per project",
                "stauts": False,
            }, status=HTTP_406_NOT_ACCEPTABLE)

        data["project"] = project_obj.pk
        data["token"] = str(uuid4())

        project_token_serializer = TokenSerializer(data=data)

        if project_token_serializer.is_valid():
            project_token_obj = project_token_serializer.save()

            if project_token_obj.pk:
                return JsonResponse({
                    "message": "successfully created new project token for {}".format(project_obj.project_name),
                    "project": project_obj.project_name,
                    "project_id": project_obj.project_id,
                    "token": project_token_obj.token,
                    "status": True,
                }, status=HTTP_201_CREATED)
            else:
                return JsonResponse({
                    "message": "Error occurred creating new project token.",
                    "status": False
                }, status=HTTP_400_BAD_REQUEST)
        else:
            # Error
            return JsonResponse({
                "message": "Error occurred creating new project token. {}".format(project_token_serializer.errors),
                "status": False
            }, status=HTTP_400_BAD_REQUEST)
