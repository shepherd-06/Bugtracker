from user.models import CustomUser
from organization.models import Organization


def get_user_object(email=None, username=None):
    try:
        if email is not None:
            return CustomUser.objects.get(email=email)
        elif username is not None:
            return CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # Token Invalid
        return None

def get_org_object(org_id):
    try:
        return Organization.objects.get(org_id=org_id)
    except Organization.DoesNotExist:
        return None