from django.db import DataError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from bugtracker.model_managers.serializer import OrgSerializer
from bugtracker.models import Organisation, Projects, UserToOrg
from bugtracker.utility import (authorization_token_check, error_occurred,
                                get_org_object, get_token_object_by_token,
                                invalid_user, organization_not_found,
                                token_invalid, unauthorized_access)


class Org(APIView):

    def post(self, request):
        data = request.data
        token_obj = authorization_token_check(data)
        if type(token_obj) == JsonResponse:
            return token_obj

        user_obj = token_obj.authorized_user
        if not user_obj.is_admin:
            return JsonResponse(unauthorized_access, status=status.HTTP_401_UNAUTHORIZED)

        if "org_name" not in data:
            return JsonResponse({
                "message": "Missing mandatory parameter, {org_name}",
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "org_name": data["org_name"],
            "created_by": user_obj.pk,
        }

        org_serializer = OrgSerializer(data=payload)
        if org_serializer.is_valid():
            try:
                org_obj = org_serializer.save()

                return JsonResponse({
                    "message": "A new organization, [ {} ] has been created".format(org_obj.org_name),
                    "org_id": org_obj.org_id,
                    "org_name": org_obj.org_name,
                    "created_by": org_obj.created_by.email,
                    "created_at": org_obj.created_at,
                    "updated_at": org_obj.updated_at,
                    "status": status.HTTP_201_CREATED,
                }, status=status.HTTP_201_CREATED)
            except Exception: 
                Organisation.objects.filter(org_id=org_obj.org_id).delete()
                return JsonResponse({
                    "message": "An error occurred! {}".format(org_serializer.errors),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            Organisation.objects.filter(org_id=org_obj.org_id).delete()
            return JsonResponse({
                "message": "An error occurred! {}".format(org_serializer.errors),
                "status": status.HTTP_406_NOT_ACCEPTABLE
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

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
        data = request.data
        org_id = pk
        token_obj = authorization_token_check(data)
        if type(token_obj) == JsonResponse:
            return token_obj

        user_obj = token_obj.authorized_user
        if not user_obj.is_admin:
            return JsonResponse(unauthorized_access)

        if "org_name" not in data:
            return JsonResponse({
                "message": "Missing mandatory parameter. {org_name} is required!",
                "status": status.HTTP_400_BAD_REQUEST
            })

        organization = get_org_object(str(org_id))
        if organization is None:
            return JsonResponse(organization_not_found)

        try:
            organization.org_name = data['org_name']
            organization.save()
            return JsonResponse({
                "message": "Successfully updated organization detail",
                "id": organization.pk,
                "org_id": organization.org_id,
                "org_name": organization.org_name,
                "created_by": organization.created_by.user_email,
                "created_at": organization.created_at,
                "updated_at": organization.updated_at,
                "status": status.HTTP_202_ACCEPTED
            })
        except ValidationError as error:
            return JsonResponse({
                "message": "Error occurred! {}".format(error),
                "status": status.HTTP_406_NOT_ACCEPTABLE
            })
        except DataError as error:
            return JsonResponse({
                "message": "Error occurred! {}".format(error),
                "status": status.HTTP_406_NOT_ACCEPTABLE
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
        data = request.data
        org_id = pk
        token_obj = authorization_token_check(data)
        if type(token_obj) == JsonResponse:
            return token_obj

        user_obj = token_obj.authorized_user
        if not user_obj.is_admin:
            return JsonResponse(unauthorized_access)

        organization = get_org_object(str(org_id))
        if organization is None:
            return JsonResponse(organization_not_found)

        # see if there is any entry of this organization in project or error table
        project_queryset = Projects.objects.filter(
            organization=organization.pk)
        if project_queryset.count() > 0:
            # remove not possible
            return JsonResponse({
                "message": "Organization cannot be deleted. This org is in use to one/multiple project(s)",
                "status": status.HTTP_403_FORBIDDEN
            })

        # Delete all entry from User_To_Org entry
        user_to_org_obj = UserToOrg.objects.filter(
            organization=organization.pk)
        user_removed = 0
        for entry in user_to_org_obj:
            entry_delete = entry.delete()
            if entry_delete:
                user_removed += 1

        delete_status = organization.delete()

        if delete_status:
            return JsonResponse({
                "message": "Organization: {} removed successfully.".format(organization.org_name),
                "user_removed": user_removed,
                "status": status.HTTP_200_OK
            })
        else:
            return JsonResponse(error_occurred)

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

        if pk is None:
            all_orgs = Organisation.objects.all()
            payload = list()

            for orgs in all_orgs:
                total_members = UserToOrg.objects.filter(
                    organization=orgs.pk).count()
                payload.append({
                    'org_id': orgs.org_id,
                    "org_name": orgs.org_name,
                    "created_by": orgs.created_by.user_email,
                    "created_at": orgs.created_at,
                    "updated_at": orgs.updated_at,
                    "total_members": total_members,
                })

            return JsonResponse({
                "payload": payload,
                "status": status.HTTP_200_OK,
            })
        else:
            org_obj = get_org_object(pk)
            if org_obj is None:
                return JsonResponse(organization_not_found)

            return JsonResponse({
                'org_id': org_obj.org_id,
                "org_name": org_obj.org_name,
                "created_by": org_obj.created_by.user_email,
                "created_at": org_obj.created_at,
                "updated_at": org_obj.updated_at,
                "total_members": UserToOrg.objects.filter(organization=org_obj.pk).count(),
                "status": status.HTTP_200_OK,
            }
            )
