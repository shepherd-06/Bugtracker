from django.core.exceptions import ValidationError
from rest_framework.views import APIView

from bugtracker.model_managers.models import UserToken
from bugtracker.model_managers.serializer import ErrorSerializer


class ErrorByUser(APIView):

    @staticmethod
    def get_user_token_validation(user_token):
        try:
            token_obj = UserToken.objects.get(token=user_token)
            return token_obj.authorized_user
        except UserToken.DoesNotExist:
            # User Token does not exist
            return None
        except ValidationError:
            # User Token does not exist
            return None

    def post(self, request):
        data = request.data
        if 'token' not in data:
            # Error
            pass
        user_id = self.get_user_token_validation(data['token'])
        if user_id is None:
            # Token invalid
            pass

        # serializer = ErrorSerializer(data=data)
        # if serializer.is_valid():
        #     _ = serializer.save()
        #     return JsonResponse({
        #         "message": "Error logged successfully",
        #         "id": _._id,
        #         'status': http_status.HTTP_201_CREATED,
        #     })
        # else:
        #     return JsonResponse({
        #         'message': serializer.errors,
        #         'status': http_status.HTTP_400_BAD_REQUEST
        #     })

