import uuid

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.model_managers.models import ProjectToken, Projects
from bugtracker.model_managers.serializer import ProjectTokenSerializer
from bugtracker.utility import authorization_token_check, get_project_from_project_id, project_not_found, \
    get_usr_to_org_by_user_id_and_org_id, unauthorized_access, error_occurred, token_invalid, get_token_object_by_token, \
    invalid_user, get_all_org_user_is_part_off


class ProjectTokenCRUD(APIView):
    """
    Anybody who has access to organization of the project can create a token. But that will
    invalidate the previous token
    """

    def post(self, request):
        data = request.data

        token_obj = authorization_token_check(data)
        if type(token_obj) == JsonResponse:
            return token_obj

        user_obj = token_obj.authorized_user

        if "project_id" not in data:
            return JsonResponse({
                "message": "Missing required parameter. {project_id} is required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        project_obj = get_project_from_project_id(data["project_id"])
        if project_obj is None:
            return JsonResponse(project_not_found)

        organization = project_obj.organization
        if get_usr_to_org_by_user_id_and_org_id(user_obj.pk, organization.pk).count() != 1:
            return JsonResponse(unauthorized_access)

        # If count() is 1, that means this user is part of this organization.
        # And user can create a project token for this organization
        project_token_serializer = ProjectTokenSerializer(data={
            "project": project_obj.pk
        })

        if project_token_serializer.is_valid():
            project_token_obj = project_token_serializer.save()

            if project_token_obj.pk:
                return JsonResponse({
                    "message": "successfully created new project token for {}".format(project_obj.project_name),
                    "project": project_obj.project_name,
                    "project_id": project_obj.project_id,
                    "token": project_token_obj.token,
                    "refresh_token": project_token_obj.refresh_token,
                    "time_to_live": project_token_obj.time_to_live,
                    "status": status.HTTP_201_CREATED,
                })
            else:
                return JsonResponse(error_occurred)
        else:
            # Error
            return JsonResponse({
                "message": "Error occurred creating new project token. {}".format(project_token_serializer.errors),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            })

    """
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    """

    def put(self, request, project_token):
        """
        this is project token renewal. This would be completely automated via zathura package
        :param request: request obj.
        :param project_token: project_token
        :return: new project_token with refresh_token
        """
        data = request.data

        if "project_id" not in data or "refresh_token" not in data:
            return JsonResponse({
                "message": "Missing parameters. {project_id} and {refresh_token} are both required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        # Get project obj first
        project_obj = get_project_from_project_id(data["project_id"])

        try:
            project_token_obj = ProjectToken.objects.get(project=project_obj.pk,
                                                         token=uuid.UUID(project_token),
                                                         refresh_token=uuid.UUID(data["refresh_token"])
                                                         )

            if project_token_obj.pk:
                project_token_obj.save()
                return JsonResponse({
                    "message": "Renewed project token for {}".format(project_token_obj.project.project_name),
                    "token": project_token_obj.token,
                    "refresh_token": project_token_obj.refresh_token,
                    "project": project_token_obj.project.project_name,
                    "status": status.HTTP_202_ACCEPTED,
                })

        except ProjectToken.DoesNotExist:
            return JsonResponse({
                "message": "This project token does not exist",
                "status": status.HTTP_404_NOT_FOUND
            })
        except ValueError as error:
            return JsonResponse({
                "message": "An error occurred. {}".format(error),
                "status": status.HTTP_404_NOT_FOUND
            })

    """
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    """

    def delete(self, request, project_token):
        """
        Only an admin can delete a project token
        One can only delete a project token from the web/admin panel. Can not do it via zathura
        :param request: request
        :param project_token: project_token to delete
        :return: success/error message
        """
        data = request.data
        token_obj = authorization_token_check(data)
        if type(token_obj) == JsonResponse:
            return token_obj

        user_obj = token_obj.authorized_user

        if not user_obj.is_admin:
            return JsonResponse(unauthorized_access)

        if "project_id" not in data:
            return JsonResponse({
                "message": "Missing parameters. {project_id} is both required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        # Get project obj first
        project_obj = get_project_from_project_id(data["project_id"])

        try:
            project_token_obj = ProjectToken.objects.get(project=project_obj.pk,
                                                         token=uuid.UUID(project_token))

            if project_token_obj.pk:
                project_token_obj.delete()

                return JsonResponse({
                    "message": "Successfully removed project token for project: {}".format(project_token_obj.project.project_name),
                    "status": status.HTTP_202_ACCEPTED
                })
        except ProjectToken.DoesNotExist:
            return JsonResponse({
                "message": "This project token does not exist",
                "status": status.HTTP_404_NOT_FOUND
            })
        except ValueError as error:
            return JsonResponse({
                "message": "An error occurred. {}".format(error),
                "status": status.HTTP_404_NOT_FOUND
            })

    """
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    ---------------------------------------------------
    """

    def get(self, request):
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        token_obj = get_token_object_by_token(token)
        if token_obj is None:
            return JsonResponse(invalid_user)

        # send all tokens generated by the users organization
        # if user is an admin, send all tokens.

        user_obj = token_obj.authorized_user

        if user_obj.is_admin:
            all_project_tokens = ProjectToken.objects.all()

            data = list()

            for project_token in all_project_tokens:
                data.append({
                    "project": project_token.project.project_name,
                    "project_description": project_token.project.project_description,
                    "project_token": project_token.token,
                    "generated_at": project_token.generated_at,
                    "updated_at": project_token.updated_at,
                    "organization": project_token.project.organization.org_name,
                })

            return JsonResponse({
                "data": data,
                "status": status.HTTP_200_OK
            }) 
        else:
            # user is not admin
            # get organization user is part of
            all_org_query_set = get_all_org_user_is_part_off(user_obj.user_id)

            data = list()
            for orgs in all_org_query_set:

                # now get all the projects of this organization
                all_projects = Projects.objects.filter(organization=orgs.organization.pk)

                for project in all_projects:
                    # now get the project_token of this project
                    project_token_obj = ProjectToken.objects.get(project=project.pk)
                    data.append({
                        "project": project.project_name,
                        "project_description": project.project_description,
                        "project_token": project_token_obj.token,
                        "generated_at": project_token_obj.generated_at,
                        "updated_at": project_token_obj.updated_at,
                        "organization": orgs.organization.org_name,
                    })
            return JsonResponse({
                "data": data,
                "status": status.HTTP_200_OK
            })
