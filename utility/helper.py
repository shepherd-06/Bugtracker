from user.models import CustomUser
from organization.models import Organization
from projects.models import Projects
from token_manager.models import ProjectToken


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
    
def get_project_object(project_id):
    try:
        return Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return None
    
def get_project_token_by_project_id(project):
    try:
        return ProjectToken.objects.get(project=project)
    except ProjectToken.DoesNotExist:
        return None