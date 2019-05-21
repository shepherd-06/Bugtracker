from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.model_managers.serializer import ProjectSerializer, ProjectUpdateSerializer, Projects
from bugtracker.utility import get_token_object_by_token, token_invalid


class Project(APIView):
    """
    Project cannot be added with access token.
    Project will have registered_by field. I can get that from user_token
    Project will have project_name and description from the user_input.
    """

    def post(self, request):
        """
        mandatory field: user_token, project_name
        :param request: django request obj
        :return: JSONResponse
        """
        data = request.data

        if 'token' not in data or 'project_name' not in data:
            return JsonResponse({
                "message": "Missing parameters! token, project_name is required",
                "status": status.HTTP_400_BAD_REQUEST
            })
        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse({
                "message": "Invalid User!",
                "status": status.HTTP_401_UNAUTHORIZED
            })
        user_object = token_obj.authorized_user
        payload = {
            "registered_by": user_object.user_id,
            "project_name": data['project_name'],
            "project_description": data["project_description"] if "project_description" in data else None,
        }

        project_serializer = ProjectSerializer(data=payload)

        try:
            if project_serializer.is_valid():
                project = project_serializer.save()
                if project is not None:
                    payload = {
                        "project": project._id,
                        "updated_by": user_object.user_id
                    }
                    project_update_serializer = ProjectUpdateSerializer(data=payload)
                    if project_update_serializer.is_valid():
                        project_update = project_update_serializer.save()
                        if project_update.pk:
                            # success
                            return JsonResponse({
                                "message": "successfully added a new project",
                                "project_id": project.pk,
                                "project_name": project.project_name,
                                "description": project.project_description,
                                "registered_at": project.registered_at,
                                "registered_by": user_object.user_email,
                                "updated_by": project_update.updated_by.user_email,
                                "updated_at": project_update.updated_at,
                                "status": status.HTTP_201_CREATED,
                            })
                        else:
                            # Error
                            Projects.objects.filter(_id=project.pk).delete()
                            return JsonResponse({
                                "message": "Failed to create a new project",
                                "status": status.HTTP_400_BAD_REQUEST
                            })
                    else:
                        print("---------------------------")
                        print("project_update_serializer: {}".format(project_update_serializer.errors))
                        print("---------------------------")
                        return JsonResponse({
                            "message": "Failed to create a new project",
                            "status": status.HTTP_400_BAD_REQUEST
                        })
                else:
                    return JsonResponse({
                        "message": "Failed to create a new project",
                        "status": status.HTTP_400_BAD_REQUEST
                    })
            else:
                print("---------------------------")
                print("project_serializer: {}".format(project_serializer.errors))
                print("---------------------------")
                return JsonResponse({
                    "message": "Failed to create a new project",
                    "status": status.HTTP_400_BAD_REQUEST
                })
        except ValidationError as error:
            return JsonResponse({
                "message": "{}".format(error),
                "status": status.HTTP_401_UNAUTHORIZED
            })

    def get(self, request):
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        token_obj = get_token_object_by_token(token)
        if token_obj is None:
            return JsonResponse({
                "message": "Invalid User!",
                "status": status.HTTP_401_UNAUTHORIZED
            })
        user_object = token_obj.authorized_user
        all_projects = Projects.objects.filter(registered_by=user_object.user_id).all()

        return JsonResponse({
            "total": len(list(all_projects)),
            "projects" : list(all_projects),
            "status": status.HTTP_200_OK
        })
