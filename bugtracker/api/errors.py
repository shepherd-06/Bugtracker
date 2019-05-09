from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status as http_status

from bugtracker.model_managers.models import ProjectToken, Errors
from bugtracker.model_managers.serializer import ErrorSerializer
from bugtracker.utility import *
from zathura_bugtracker.custom_auth import TokenAuth


class Error(TokenAuth):

    @staticmethod
    def get_error_obj(error_id = None):
        try:
            if error_id is not None:
                return Errors.objects.get(_id=error_id)
            else:
                return Errors.objects.values()
        except Errors.DoesNotExist:
            return None
        except ValidationError:
            return None

    @staticmethod
    def get_project(token):
        try:
            project_token = ProjectToken.objects.get(token=token)
            return project_token.project._id
        except ProjectToken.DoesNotExist:
            # Token Invalid
            return -1
        except ValidationError:
            # Token Invalid
            return -1

    def post(self, request):
        token = request.data["token"] if "token" in request.data else None
        if token is None:
            return JsonResponse(token_invalid)
        status = super().token_validate(token)
        if status == -1:
            return JsonResponse(token_invalid)
        elif status == 1:
            return JsonResponse(token_expired)
        else:
            # This part is valid actually. It must not return Invalid status.
            # This part is for testing right now.
            # Token is already here
            payload = request.data
            token = payload['token']
            payload.pop('token')
            project_id = self.get_project(token)
            payload['reference_project'] = project_id

            serializer = ErrorSerializer(data=payload)
            if serializer.is_valid():
                _ = serializer.save()
                return JsonResponse({
                    "message": "Error logged successfully",
                    "id": _._id,
                    'status': http_status.HTTP_201_CREATED,
                })
            else:
                return JsonResponse({
                    'message': serializer.errors,
                    'status': http_status.HTTP_400_BAD_REQUEST
                })

    def put(self, request):
        token = request.data["token"] if "token" in request.data else None
        if token is None:
            return JsonResponse(token_invalid)
        status = super().token_validate(token)
        if status == -1:
            return JsonResponse(token_invalid)
        elif status == 1:
            return JsonResponse(token_expired)
        else:
            # This part is valid actually. It must not return Invalid status.
            # This part is for testing right now.
            # Token is already here
            payload = request.data
            error_id = payload['error_id']

            error_obj = self.get_error_obj(error_id)
            if 'is_resolved' in payload:
                error_obj.is_resolved = payload['is_resolved']
            if 'resolved_at' in payload:
                error_obj.resolved_at = payload['resolved_at']
            if 'resolved_by' in payload:
                error_obj.resolved_by = payload['resolved_by']
            if 'warning_level' in payload:
                error_obj.warning_level = payload['warning_level']
            error_obj.updated_at = timezone.now()
            error_obj.save()
            return JsonResponse({
                "message": "Error obj updated successfully",
                "error_id": error_id,
                'status': http_status.HTTP_202_ACCEPTED
            })

    def get(self, request):
        token = request.GET.get('token', None)
        if token is None:
            return JsonResponse(token_invalid)

        status = super().token_validate(token)
        if status == -1:
            return JsonResponse(token_invalid)
        elif status == 1:
            return JsonResponse(token_expired)
        else:
            # This part is valid actually. It must not return Invalid status.
            # This part is for testing right now.
            all_errors = list(self.get_error_obj())
            return JsonResponse({
                "total": len(all_errors),
                "errors": all_errors,
                'status': http_status.HTTP_200_OK
            })
