import uuid

from django.core.exceptions import ValidationError
from rest_framework import status

from bugtracker.model_managers.models import UserToken, User, UserToOrg, Organisation, Projects

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


def get_usr_to_org_by_user_id_and_org_id(user_id, org_primary_key):
    """
    returns UserToOrg mapping object with user_id and org_primary_key
    :param org_primary_key: Primary key of organization table.
    :param user_id: current user_id
    :return: UserToOrg or None
    """
    try:
        return UserToOrg.objects.filter(organization=uuid.UUID(org_primary_key),
                                        user=uuid.UUID(user_id))
    except UserToOrg.DoesNotExist:
        return None
    except ValidationError:
        return None
    except ValueError:
        return None


def get_all_org_user_is_part_off(user_id: str):
    """
    this function will return UserToOrg mapping queryset object where user is part of that org
    :param user_id:
    :return:
    """
    try:
        return UserToOrg.objects.filter(user=uuid.UUID(user_id))
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


def get_project_from_project_id(project_id: str):
    """
    returns project_obj from project_id
    :param project_id:
    :return:
    """
    try:
        return Projects.objects.get(project_id=uuid.UUID(str(project_id)))
    except Projects.DoesNotExist:
        return None
    except ValidationError:
        return None
    except ValueError:
        return None