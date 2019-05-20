import uuid

from django.core.exceptions import ValidationError
from rest_framework import status

from bugtracker.model_managers.models import UserToken, User

token_expired = {
    'message': 'token_expired',
    'status_code': -100,
    'status': status.HTTP_406_NOT_ACCEPTABLE
}

token_invalid = {
    'message': 'token invalid',
    'status_code': -101,
    'status': status.HTTP_401_UNAUTHORIZED
}


def get_user_object(user_id):
    try:
        user = User.objects.get(user_id=uuid.UUID(user_id))
        return user
    except User.DoesNotExist:
        # Token Invalid
        return None
    except ValidationError:
        # Token Invalid
        return None
    except ValueError:
        return None


def get_user_token(user):
    try:
        token_obj = UserToken.objects.get(authorized_user=user)
        return token_obj
    except UserToken.DoesNotExist:
        # User Token does not exist
        return None
    except ValidationError:
        # User Token does not exist
        return None
