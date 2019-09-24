from uuid import uuid4

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)
from rest_framework.views import APIView

from projects.serializer import ProjectSerializer
from utility.helper import get_org_object, get_user_object


class ProjectCRUD(APIView):

    failed_to_create_project = {
        "message": "Failed to create a new project",
        "status": False,
    }

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        """
        mandatory field: user_token, project_name, organization_id
        from the user_token, get the user_id and check if user is part of this org.
        if yes. then Okay else Validation Error
        :param request: django request obj
        :return: JSONResponse
        """
        data = request.data

        if 'project_name' not in data or "organization_id" not in data:
            return JsonResponse({
                "message": "Missing parameters! project_name and organization_id are required",
                "status": HTTP_400_BAD_REQUEST
            })
        
        user = get_user_object(username=request.user.username)
        # TODO: check if user is an admin to create a project under this org.

        org_object = get_org_object(data["organization_id"])
        if org_object is None:
            return JsonResponse({
                "status": False,
                "message": "Organization does not exist."
            }, status=HTTP_400_BAD_REQUEST)

        payload = {
            "project_id": str(uuid4())[:12],
            "organization": org_object.pk,
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
                        "organization": org_object.org_name,
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
