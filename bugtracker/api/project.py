from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from bugtracker.utility import get_user_token, get_user_object, get_token_object_by_token


class Project(APIView):

    """
    Project cannot be added with access token.
    Project will have registered_by field. I can get that from user_token
    Project will have project_name and description from the user_input.
    """

    def post(self, request):
        """
        mandatory field: user_token, project_name and project_description
        :param request: django request obj
        :return: JSONResponse
        """
        data = request.data

        if 'token' not in data or 'project_name' not in data or 'project_description' not in data:
            return JsonResponse({
                "message": "Missing parameters! token, project_name and project_description is required",
                "status": status.HTTP_400_BAD_REQUEST
            })
        token_obj = get_token_object_by_token(data['token'])
        if token_obj is None:
            return JsonResponse({
                "message": "Invalid User!",
                "status": status.HTTP_401_UNAUTHORIZED
            })
        user_object = token_obj.authorized_user
        # Need to check if the project name and description pass the criteria.
        # Do check them through validator in serializer (may be, will be time saver)
        payload = {

        }
