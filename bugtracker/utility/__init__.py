import uuid

from django.core.exceptions import ValidationError
from rest_framework import status

from bugtracker.model_managers.models import UserToken, User, UserToOrg, Organisation

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


def get_token_object_by_token(user_token):
    try:
        token_obj = UserToken.objects.get(token=uuid.UUID(user_token))
        return token_obj
    except UserToken.DoesNotExist:
        # User Token does not exist
        return None
    except ValidationError:
        # User Token does not exist
        return None
    except ValueError:
        return None


def get_usr_to_org_by_user_id_and_org_id(user_id, org_id):
    """
    returns UserToOrg mapping object with user_id and org_id
    :param user_id: current user_id
    :param org_id: current org_id
    :return: UserToOrg or None
    """
    try:
        return UserToOrg.objects.filter(organization=uuid.UUID(org_id),
                                        user=uuid.UUID(user_id))
    except UserToOrg.DoesNotExist:
        return None
    except ValidationError:
        return None
    except ValueError:
        return None


def get_org_object(org_id: str):
    """
    returns organisation object from the org_id
    :param org_id:
    :return:
    """
    try:
        return Organisation.objects.get(org_id=uuid.UUID(org_id))
    except Organisation.DoesNotExist:
        return None
    except ValueError:
        return None
    except ValidationError:
        return None
