from user.models import CustomUser


def get_user_object(email=None, username=None):
    try:
        if email is not None:
            return CustomUser.objects.get(email=email)
        elif username is not None:
            return CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # Token Invalid
        return None
