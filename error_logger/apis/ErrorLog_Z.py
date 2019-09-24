from uuid import uuid4

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView

from error_logger.serializer import ErrorLoggerSerializer
from utility.helper import get_project_token_object, get_project_object
from datetime import datetime


class ErrorLogByPackage(APIView):

    required_fields = ("project_token", "error_name",
                       "error_description",
                       "point_of_origin")

    def post(self, request):
        data = request.data

        for field in self.required_fields:
            if field not in data:
                return JsonResponse({
                    "message": "Missing mandatory parameters. {} is required".format(field),
                    "status": False,
                }, status=HTTP_400_BAD_REQUEST)

        project_token_obj = get_project_token_object(data["project_token"])

        if project_token_obj is None:
            return JsonResponse({
                "message": "Project token does not exist",
                "status": False
            }, status=HTTP_401_UNAUTHORIZED)
        data["reference_project"] = project_token_obj.project.pk

        error_log_serializer = ErrorLoggerSerializer(data=data)
        if error_log_serializer.is_valid():
            error_log_obj = error_log_serializer.save()
            project_token_obj.last_access = datetime.utcnow()
            project_token_obj.save()

            return JsonResponse({
                "message": "successfully logged error: {}".format(error_log_obj.error_name),
                "status": True,
                "logged_on": error_log_obj.logged_on,
                "reference_project": error_log_obj.reference_project.project_name,
                "warning_level": error_log_obj.warning_level,
            })
        else:
            return JsonResponse({
                "message": "An error occurred! {}".format(error_log_serializer.errors),
                "status": False,
            }, status=HTTP_406_NOT_ACCEPTABLE)
