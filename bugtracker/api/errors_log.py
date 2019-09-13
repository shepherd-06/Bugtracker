import uuid

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.models import Errors, ErrorStatus
from bugtracker.model_managers.serializer import ErrorSerializer, ErrorStatusSerializer
from bugtracker.utility import get_token_object_by_token, get_project_token_object_by_token, token_invalid, \
    error_occurred, invalid_user, error_not_found, get_project_from_project_id, missing_token_parameter, \
    unauthorized_access, get_error_object_from_error_id


class ErrorLog(APIView):

    @staticmethod
    def error_token_authorization(data):
        if 'token' in data:
            return get_token_object_by_token(data['token'])
        else:
            return get_project_token_object_by_token(data['project_token'])

    def post(self, request):
        """
        An Error can be logged by two ways.
        1) From the app/project using the project_api_keys. Issued_by field will ne None, in this case
        2) By an admin/user using token. reference_project field can be filled (optional) by user in this case
        so either of token or project_token has to be present on the request.data
        :param request:
        :return:
        """
        data = request.data

        if 'token' not in data and 'project_token' not in data:
            # un-authorized
            return JsonResponse(
                {
                    "message": "Missing mandatory parameters! token or project_token,"
                               " one of them is required",
                    "status": status.HTTP_401_UNAUTHORIZED
                }
            )
        # token authorization
        authorization_data = self.error_token_authorization(data)
        if authorization_data is None:
            return JsonResponse(token_invalid)

        if 'error_name' not in data or 'description' not in data or 'origin' not in data:
            # missing mandatory parameter
            return JsonResponse({
                "message": "Missing mandatory parameter. error_name, description and origin are required",
                "status": status.HTTP_400_BAD_REQUEST
            })

        payload = dict()
        if 'token' in data:
            payload['issued_by'] = authorization_data.authorized_user.pk
            if 'project_token' in data:
                # get the reference project object from the database using the UUID of the project
                project_token_obj = get_project_token_object_by_token(data['project_token'])
                if project_token_obj is not None:
                    payload['reference_project'] = project_token_obj.project.pk
        else:
            payload['reference_project'] = authorization_data.project.pk

        payload['error_name'] = data['error_name']
        payload['error_description'] = data['description']
        payload['error_description'] = data['description']
        payload['point_of_origin'] = data['origin']

        if 'warning_level' in data:
            payload['warning_level'] = data['warning_level']

        error_log_serializer = ErrorSerializer(data=payload)
        if error_log_serializer.is_valid():
            error_log_obj = error_log_serializer.save()

            if error_log_obj.pk:
                return JsonResponse({
                    "message": "successfully logged error: {}".format(error_log_obj.error_name),
                    "status": status.HTTP_201_CREATED,
                    "error_name": error_log_obj.error_name,
                    "description": error_log_obj.error_description,
                    "origin": error_log_obj.point_of_origin,
                    "logged_at": error_log_obj.logged_at,
                    "issued_by": error_log_obj.issued_by.user_email if error_log_obj.issued_by is not None else None,
                    "reference_project": error_log_obj.reference_project.project_name,
                    "warning_level": error_log_obj.warning_level,
                })
            else:
                return JsonResponse(error_occurred)
        else:
            return JsonResponse({
                "message": "An error occurred! {}".format(error_log_serializer.errors),
                "status": status.HTTP_406_NOT_ACCEPTABLE
            })

    def get(self, request, error_pk=None):
        """
        TODO: 1) pagination 2) filtering by (origin, project, logged_time, issued_by, is_resolved)
        a get request can only be made from the web.
        :param request:
        :param error_pk: if it's not None, then an individual error has been requested
        :return: dict
        """
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        token_obj = get_token_object_by_token(token)
        if token_obj is None:
            return JsonResponse(invalid_user)

        if error_pk is not None:
            # get a single error_obj and return it.
            try:
                error_object = Errors.objects.get(_id=uuid.UUID(error_pk))
                error_updates = list()
                # get the objects from ErrorStatus table

                error_status_queryset = ErrorStatus.objects.filter(error=error_object.pk)
                for entry in error_status_queryset:
                    error_updates.append({
                        "resolved_by": entry.resolved_by.user_email,
                        "resolved_at": entry.resolved_at,
                        "updated_at": entry.updated_at,
                    })

                return JsonResponse({
                    "error_id": error_object.pk,
                    "error_name": error_object.error_name,
                    "description": error_object.error_description,
                    "origin": error_object.point_of_origin,
                    "logged_at": error_object.logged_at,
                    "is_resolved": error_object.is_resolved,
                    "issued_by": error_object.issued_by.user_email if error_object.issued_by is not None else None,
                    "warning_level": error_object.warning_level,
                    "reference_project": error_object.reference_project.project_name if error_object.reference_project is not None else None,
                    "updates": error_updates,
                    "status": status.HTTP_200_OK
                })
            except Errors.DoesNotExist:
                return JsonResponse(error_not_found)
            except ValueError:
                return JsonResponse(error_not_found)
        else:
            all_errors = Errors.objects.all()
            payload = list()
            for single_error in all_errors:
                error_updates = list()
                # get the objects from ErrorStatus table

                error_status_queryset = ErrorStatus.objects.filter(error=single_error.pk)
                for entry in error_status_queryset:
                    error_updates.append({
                        "resolved_by": entry.resolved_by.user_email,
                        "resolved_at": entry.resolved_at,
                        "updated_at": entry.updated_at,
                    })
                payload.append({
                    "error_id": single_error.pk,
                    "error_name": single_error.error_name,
                    "description": single_error.error_description,
                    "origin": single_error.point_of_origin,
                    "logged_at": single_error.logged_at,
                    "is_resolved": single_error.is_resolved,
                    "issued_by": single_error.issued_by.user_email if single_error.issued_by is not None else None,
                    "warning_level": single_error.warning_level,
                    "reference_project": single_error.reference_project.project_name if single_error.reference_project is not None else None,
                    "updates": error_updates
                })
            return JsonResponse({
                "status": status.HTTP_200_OK,
                "errors": payload
            })

    def put(self, request, error_pk):
        """

        :param request:
        :param error_pk:
        :return:
        """
        data = request.data

        if 'token' not in data:
            return JsonResponse(missing_token_parameter)

        if "error_name" not in data \
                and "description" not in data \
                and "origin" not in data \
                and "warning_level" not in data \
                and "is_resolved" not in data \
                and "reference_project" not in data:
            # This condition has an error! Be Ware!
            return JsonResponse({
                "message": "Missing optional field. One of them must be present. "
                           "error_name, description, origin, warning_level, is_resolved, reference_project",
                "status": status.HTTP_400_BAD_REQUEST
            })
        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse(invalid_user)

        user_object = token_obj.authorized_user

        if error_pk is None:
            return JsonResponse(error_not_found)

        error_object = get_error_object_from_error_id(error_pk)
        if error_object is None:
            return JsonResponse(error_not_found)

        if "error_name" in data:
            error_object.error_name = data["error_name"]

        if "description" in data:
            error_object.error_description = data["description"]

        if "origin" in data:
            error_object.point_of_origin = data["origin"]

        if "warning_level" in data:
            error_object.warning_level = data["warning_level"]

        if "is_resolved" in data:
            error_object.is_resolved = data["is_resolved"]

        if "reference_project" in data:
            error_object.reference_project = get_project_from_project_id(data['reference_project'])

        # TODO: check what happens if I failed validation on error_name, description or origin field
        error_object.save()

        payload = {
            "error": error_object.pk,
            "resolved_by": user_object.pk,
        }
        error_status_serializer = ErrorStatusSerializer(data=payload)
        if error_status_serializer.is_valid():
            error_status_serializer.save()

            error_updates = list()
            # get the objects from ErrorStatus table

            error_status_queryset = ErrorStatus.objects.filter(error=error_object.pk)
            for entry in error_status_queryset:
                error_updates.append({
                    "resolved_by": entry.resolved_by.user_email,
                    "resolved_at": entry.resolved_at,
                    "updated_at": entry.updated_at,
                })

            return JsonResponse({
                "error_id": error_object.pk,
                "error_name": error_object.error_name,
                "description": error_object.error_description,
                "origin": error_object.point_of_origin,
                "logged_at": error_object.logged_at,
                "is_resolved": error_object.is_resolved,
                "issued_by": error_object.issued_by.user_email if error_object.issued_by is not None else None,
                "warning_level": error_object.warning_level,
                "reference_project": error_object.reference_project.project_name if error_object.reference_project is not None else None,
                "updates": error_updates,
                "status": status.HTTP_200_OK
            })
        else:
            return JsonResponse({
                "message": "An error occurred. {}".format(error_status_serializer.errors),
                "status": status.HTTP_406_NOT_ACCEPTABLE
            })

    def delete(self, request, error_pk):
        """
        TODO: enable multiple entry delete
        only an admin can delete a error_entry
        :param request:
        :param error_pk: primary key of this particular error_object
        :return:
        """
        data = request.data
        if 'token' not in data:
            return JsonResponse(missing_token_parameter)

        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse(invalid_user)
        user_object = token_obj.authorized_user
        if not user_object.is_admin:
            return JsonResponse(unauthorized_access)

        if error_pk is None:
            return JsonResponse(error_not_found)

        error_object = get_error_object_from_error_id(error_pk)
        if error_object is None:
            return JsonResponse(error_not_found)

        # Remove all the entry from ErrorStatus table
        all_error_status = ErrorStatus.objects.filter(error=error_object.pk)
        for entry in all_error_status:
            entry.delete()

        # now delete the actual entry.
        error_object.delete()

        if get_error_object_from_error_id(error_pk) is None:
            return JsonResponse({
                "message": "successfully deleted error",
                "status": status.HTTP_202_ACCEPTED
            })
        else:
            return JsonResponse(error_occurred)
