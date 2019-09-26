from datetime import datetime

from django.http import JsonResponse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from error_logger.serializer import VerboseLogSerializer
from utility.helper import get_project_token_object


class VerboseLogZathura(APIView):

    required_fields = ("point_of_origin",
                       "log_description",
                       "project_token",)

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

        payload = dict()
        for key in data:
            payload[key] = data[key]

        payload["reference_project"] = project_token_obj.project.pk
        verbose_serializer = VerboseLogSerializer(data=payload)

        if verbose_serializer.is_valid():
            verbose_log_obj = verbose_serializer.save()
            project_token_obj.last_access = datetime.utcnow()
            project_token_obj.save()

            return JsonResponse({
                "message": "Debug logging is a massive success",
                "status": True,
                "logged_on": verbose_log_obj.logged_on,
                "reference_project": verbose_log_obj.reference_project.project_name,
            }, status=HTTP_201_CREATED)
        else:
            return JsonResponse({
                "status": False,
                "message": "{}".format(verbose_serializer.errors),
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
