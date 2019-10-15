from uuid import uuid4

from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView

from projects.serializer import ProjectSerializer
from utility.helper import get_team_object, get_user_object
from utility.token_manager import decode_token, protected


class ProjectCRUD(View):

    failed_to_create_project = {
        "message": "Failed to create a new project",
        "status": False,
    }

    required_parameters = ("project_name", "team_id",)

    @protected
    def post(self, request):
        """
        mandatory field: user_token, project_name, team_id
        from the user_token, get the user_id and check if user is part of this org.
        if yes. then Okay else Validation Error
        :param request: django request obj
        :return: JSONResponse
        """
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        # TODO: check if user is an admin to create a project under this org.

        for field in self.required_parameters:
            if field not in request.POST:
                return JsonResponse({
                    "message": "Missing mandatory parameter, {}".format(field),
                    "status": HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)
                
        data = {
            "project_name": request.POST["project_name"],
            "team_id": request.POST["team_id"],
        }
        
        team_object = get_team_object(data["team_id"])
        if team_object is None:
            return JsonResponse({
                "status": False,
                "message": "Team does not exist."
            }, status=HTTP_400_BAD_REQUEST)

        payload = {
            "project_id": str(uuid4())[:12],
            "team": team_object.pk,
            "project_name": data['project_name'],
        }

        project_serializer = ProjectSerializer(data=payload)

        try:
            if project_serializer.is_valid():
                project = project_serializer.save()
                if project is not None:
                    return JsonResponse({
                        "message": "successfully added a new project",
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "team": team_object.team_name,
                        "status": True,
                    }, status=HTTP_201_CREATED)
                else:
                    return JsonResponse(self.failed_to_create_project, status=HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(self.failed_to_create_project, status=HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JsonResponse({
                "message": "{}".format(error),
                "status": HTTP_400_BAD_REQUEST
            })
