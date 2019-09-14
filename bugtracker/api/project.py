from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.model_managers.serializer import (Projects, ProjectSerializer,
                                                  ProjectUpdate,
                                                  ProjectUpdateSerializer)
from bugtracker.models import ProjectToken
from bugtracker.utility import (get_all_org_user_is_part_off, get_org_object,
                                get_project_from_project_id,
                                get_token_object_by_token,
                                get_usr_to_org_by_user_id_and_org_id,
                                invalid_user, missing_token_parameter,
                                organization_not_found, project_not_found,
                                token_invalid, unauthorized_access,
                                user_not_part_of_org)


class Project(APIView):
    """
    Project cannot be added with access token.
    Project will have registered_by field. I can get that from user_token
    Project will have project_name and description from the user_input.
    """

    failed_to_create_project = {
        "message": "Failed to create a new project",
        "status": status.HTTP_400_BAD_REQUEST
    }

    def post(self, request):
        """
        mandatory field: user_token, project_name, organization_id
        from the user_token, get the user_id and check if user is part of this org.
        if yes. then Okay else Validation Error
        :param request: django request obj
        :return: JSONResponse
        """
        data = request.data

        if 'token' not in data or 'project_name' not in data or "organization_id" not in data:
            return JsonResponse({
                "message": "Missing parameters! token, project_name and organization_id are required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse(invalid_user)

        user_object = token_obj.authorized_user
        if not user_object.is_admin:
            return JsonResponse(unauthorized_access)

        org_object = get_org_object(data["organization_id"])
        if org_object is None:
            return JsonResponse(organization_not_found)

        user_to_org_object = get_usr_to_org_by_user_id_and_org_id(
            str(user_object.user_id), str(org_object.pk))
        if user_to_org_object is None:
            return JsonResponse(user_not_part_of_org)

        payload = {
            "registered_by": user_object.user_id,
            "organization": org_object.pk,
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
                    project_update_serializer = ProjectUpdateSerializer(
                        data=payload)
                    if project_update_serializer.is_valid():
                        try:
                            project_update = project_update_serializer.save()
                            if project_update.pk:
                                # success
                                return JsonResponse({
                                    "message": "successfully added a new project",
                                    "project_id": project.pk,
                                    "project_name": project.project_name,
                                    "description": project.project_description,
                                    "registered_at": project.registered_at,
                                    "registered_by": user_object.email,
                                    "organization": org_object.org_name,
                                    "updated_by": project_update.updated_by.email,
                                    "updated_at": project_update.updated_at,
                                    "status": status.HTTP_201_CREATED,
                                })
                            else:
                                # Error
                                Projects.objects.filter(
                                    _id=project.pk).delete()
                                return JsonResponse(self.failed_to_create_project)
                        except Exception:
                            Projects.objects.filter(_id=project.pk).delete()
                            return JsonResponse(self.failed_to_create_project)
                    else:
                        return JsonResponse(self.failed_to_create_project)
                else:
                    return JsonResponse(self.failed_to_create_project)
            else:
                return JsonResponse(self.failed_to_create_project)
        except ValidationError as error:
            return JsonResponse({
                "message": "{}".format(error),
                "status": status.HTTP_401_UNAUTHORIZED
            })

    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    def get(self, request, pk=None):
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        token_obj = get_token_object_by_token(token)
        if token_obj is None:
            return JsonResponse(invalid_user)
        user_object = token_obj.authorized_user
        # get all organization this user is a member off.
        if pk is None:
            user_to_org_object = get_all_org_user_is_part_off(
                str(user_object.pk))
            final_projects = list()

            for entry in user_to_org_object:
                # a single entry is a organization user is part off
                all_projects_queryset = Projects.objects.all().filter(
                    organization=entry.organization)

                for project_entry in all_projects_queryset:
                    # get project updated information from project_entry value
                    project_updated_queryset = ProjectUpdate.objects.filter(
                        project=project_entry.pk)
                    project_updated_info = list()
                    for single_project_update_entry in project_updated_queryset:
                        project_updated_info.append({
                            "updated_by": single_project_update_entry.updated_by.email,
                            "updated_at": single_project_update_entry.updated_at
                        })

                    final_projects.append({
                        "project_id": project_entry.project_id,
                        "project_name": project_entry.project_name,
                        "project_description": project_entry.project_description,
                        "registered_by": project_entry.registered_by.email,
                        "registered_at": project_entry.registered_at,
                        "organization": project_entry.organization.org_name,
                        "updates": project_updated_info,
                    })

            return JsonResponse({
                "total": len(final_projects),
                "projects": final_projects,
                "status": status.HTTP_200_OK
            })
        else:
            # this will pick a single project
            project_obj = get_project_from_project_id(pk)
            if project_obj is None:
                # Error Project no found
                return JsonResponse(project_not_found)

            project_updated_queryset = ProjectUpdate.objects.filter(
                project=project_obj.pk)
            project_updated_info = list()
            for single_project_update_entry in project_updated_queryset:
                project_updated_info.append({
                    "updated_by": single_project_update_entry.updated_by.email,
                    "updated_at": single_project_update_entry.updated_at
                })
            return JsonResponse({
                "project_id": project_obj.project_id,
                "project_name": project_obj.project_name,
                "project_description": project_obj.project_description,
                "registered_by": project_obj.registered_by.email,
                "registered_at": project_obj.registered_at,
                "organization": project_obj.organization.org_name,
                "project_update_info": project_updated_info
            })

    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    def put(self, request, pk):
        """
        updates a particular project. required field is token and project_id
        changeable field: project_name, project_description, organization
        :param request:
        :return:
        """
        data = request.data
        project_id = pk

        if 'token' not in data:
            return JsonResponse(missing_token_parameter)
        if "project_name" not in data and "description" not in data and "organization" not in data:
            # This condition has an error! Be Ware!
            return JsonResponse({
                "message": "Missing optional field. One of them must be present. "
                           "Project_name, description or organization",
                "status": status.HTTP_400_BAD_REQUEST
            })
        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse(invalid_user)
        user_object = token_obj.authorized_user
        if not user_object.is_admin:
            return JsonResponse(unauthorized_access)

        # get the organization from the project and see user is allowed in this organization.
        project_obj = get_project_from_project_id(
            project_id)  # Need to change this project
        if project_obj is None:
            return JsonResponse(project_not_found)

        organization = get_org_object(str(project_obj.organization.org_id))
        if organization is None:
            return JsonResponse(organization_not_found)
        user_to_org_obj = get_usr_to_org_by_user_id_and_org_id(str(user_object.user_id),
                                                               str(organization.pk))
        if user_to_org_obj is None or user_to_org_obj.count() == 0:
            return JsonResponse(user_not_part_of_org)

        """
        First check user is part of old organization.
        Second check user is part of the new organization, if there is a new organization.
        Third, validate all other fields.
        """
        if "organization" in data:
            new_organization = get_org_object(str(data["organization"]))
            if new_organization is None:
                return JsonResponse(organization_not_found)
            user_to_org_obj = get_usr_to_org_by_user_id_and_org_id(str(user_object.user_id),
                                                                   str(new_organization.pk))
            if user_to_org_obj is not None:
                # user is allowed to change the organization of this project
                if user_to_org_obj.count() != 0:
                    project_obj.organization = new_organization
                else:
                    return JsonResponse(user_not_part_of_org)

        project_name = data["project_name"] if "project_name" in data else None
        description = data["description"] if "description" in data else None

        if project_name is not None:
            if 0 < len(project_name) <= 30:
                project_obj.project_name = project_name
            else:
                return JsonResponse({
                    "message": "Invalid! Project name must be between 1 to 30 characters long.",
                    "status": status.HTTP_400_BAD_REQUEST
                })

        if description is not None:
            if len(description) <= 500:
                project_obj.project_description = description
            else:
                return JsonResponse({
                    "message": "Invalid! Project description must be less than 500 characters!",
                    "status": status.HTTP_400_BAD_REQUEST
                })

        project_obj.save()
        if project_obj.pk:
            project_update_payload = {
                "project": project_obj.pk,
                "updated_by": user_object.pk
            }
            project_update_status = ProjectUpdateSerializer(
                data=project_update_payload)

            if project_update_status.is_valid():
                project_update = project_update_status.save()

                project_updated_queryset = ProjectUpdate.objects.all().filter(project=project_obj.pk)
                project_updated_info = list()
                for single_project_update_entry in project_updated_queryset:
                    project_updated_info.append({
                        "updated_by": single_project_update_entry.updated_by.email,
                        "updated_at": single_project_update_entry.updated_at
                    })

                if project_update.pk:
                    return JsonResponse({
                        "message": "Successfully updated!",
                        "status": status.HTTP_202_ACCEPTED,
                        "project_id": project_obj.project_id,
                        "project_name": project_obj.project_name,
                        "project_description": project_obj.project_description,
                        "registered_by": project_obj.registered_by.email,
                        "registered_at": project_obj.registered_at,
                        "organization": project_obj.organization.org_name,
                        "updates": project_updated_info,
                    })
                else:
                    # Error
                    return JsonResponse({
                        "message": "Invalid! unable to save project update information",
                        "status": status.HTTP_409_CONFLICT
                    })
            else:
                # Error
                return JsonResponse({
                    "message": "Invalid! project update serializer validation failed",
                    "error": str(project_update_status.errors),
                    "status": status.HTTP_409_CONFLICT
                })
        else:
            # Error
            return JsonResponse({
                "message": "Invalid! project [update] failed validation",
                "status": status.HTTP_409_CONFLICT
            })

    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    # --------------------------------------------------------
    def delete(self, request, pk):
        project_id = pk
        data = request.data

        if 'token' not in data:
            return JsonResponse(missing_token_parameter)

        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse(invalid_user)
        user_object = token_obj.authorized_user
        if not user_object.is_admin:
            return JsonResponse(unauthorized_access)

        # get the organization from the project and see user is allowed in this organization.
        project_obj = get_project_from_project_id(
            project_id)  # Need to change this project
        if project_obj is None:
            return JsonResponse(project_not_found)

        organization = get_org_object(str(project_obj.organization.org_id))
        if organization is None:
            return JsonResponse(organization_not_found)

        user_to_org_obj = get_usr_to_org_by_user_id_and_org_id(str(user_object.user_id),
                                                               str(organization.pk))
        if user_to_org_obj is None or user_to_org_obj.count() == 0:
            return JsonResponse(user_not_part_of_org)

        project_updated_queryset = ProjectUpdate.objects.filter(
            project=project_obj.pk).delete()
        project_token_status = ProjectToken.objects.filter(
            project=project_obj.pk).delete()
        state = project_obj.delete()

        if project_updated_queryset is None or project_token_status is None or state is None:
            return JsonResponse({
                "message": "An error occurred while deleting your project.",
                "status": status.HTTP_205_RESET_CONTENT
            })

        return JsonResponse({
            "project_status": "Project: {} deleted".format(project_obj.project_name),
            "project_updated_status": "Removed",
            "project_token_status": "Project token for: {} has been removed".format(project_obj.project_name),
            "message": "Project deleted",
            "status": status.HTTP_202_ACCEPTED
        })
