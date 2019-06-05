import uuid

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import status

from bugtracker.model_managers.models import UserToken, User, UserToOrg, Organisation, Projects, ProjectToken, Errors

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

unauthorized_access = {
    "message": "Unauthorized! Only an admin or an user with permission can perform this operation!",
    "status": status.HTTP_401_UNAUTHORIZED
}

missing_token_parameter = {
    "message": "Missing mandatory parameters! token is required",
    "status": status.HTTP_401_UNAUTHORIZED
}

invalid_user = {
    "message": "Invalid User!",
    "status": status.HTTP_401_UNAUTHORIZED
}

organization_not_found = {
    "message": "Invalid! Organization is not found!",
    "status": status.HTTP_400_BAD_REQUEST
}

user_not_part_of_org = {
    "message": "Invalid! User is not part of this organization!",
    "status": status.HTTP_401_UNAUTHORIZED
}

error_occurred = {
    "message": "An error occurred!",
    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
}

project_not_found = {
    "message": "Invalid! Project not found",
    "status": status.HTTP_400_BAD_REQUEST
}

error_not_found = {
    "message": "Invalid. This particular error entry does not exist.",
    "status": status.HTTP_404_NOT_FOUND
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
        token_obj = UserToken.objects.get(token=uuid.UUID(str(user_token)))
        return token_obj
    except UserToken.DoesNotExist:
        # User Token does not exist
        return None
    except ValidationError:
        # User Token does not exist
        return None
    except ValueError:
        return None


def get_project_token_object_by_token(project_token):
    try:
        return ProjectToken.objects.get(token=uuid.UUID(str(project_token)))
    except ProjectToken.DoesNotExist:
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
        return UserToOrg.objects.filter(organization=uuid.UUID(str(org_primary_key)),
                                        user=uuid.UUID(str(user_id)))
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
        return UserToOrg.objects.filter(user=uuid.UUID(str(user_id)))
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


def authorization_token_check(data: dict):
    """
    checks the validity of auth token of any request. Returns either JSON response for invalid token
    or User model object
    :param data: incoming request
    :return:
    """
    if 'token' not in data:
        return JsonResponse(missing_token_parameter)

    token_obj = get_token_object_by_token(data['token'])
    if token_obj is None:
        return JsonResponse(invalid_user)
    return token_obj


def get_error_object_from_error_id(error_id: str):
    """
    returns error_object from error_id
    :param error_id: primary key of Errors tables
    :return: Errors Object
    """
    try:
        return Errors.objects.get(_id=uuid.UUID(error_id))
    except Errors.DoesNotExist:
        return None
    except ValueError:
        return None
