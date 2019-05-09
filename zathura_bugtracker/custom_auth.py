from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.views import APIView

from bugtracker.model_managers.models import ProjectToken


class TokenAuth(APIView):

    @staticmethod
    def token_validate(token):
        """
        this functions takes the custom generated token for a project and authenticate
        aka checks its validity against the ProjectToken model.
        :param token: token parameter from the url.
        :return: -1, 0, 1 for Invalid, Valid , Expired token
        """
        try:
            project_token = ProjectToken.objects.get(token=token)
        except ProjectToken.DoesNotExist:
            # Token Invalid
            return -1
        except ValidationError:
            # Token Invalid
            return -1

        if project_token.generated_at + timedelta(seconds=project_token.time_to_live) > timezone.now():
            # Token valid
            return 0
        else:
            # Token Expired
            return 1
