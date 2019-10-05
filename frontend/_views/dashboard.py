from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from utility.token_manager import decode_token, protected
from utility.helper import get_user_object, set_cookie
from organization.models import Organization
from projects.models import Projects
# Create your views here.


class Dashboard(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        orgs = Organization.objects.filter(members__pk=user.pk)

        org_payload = list()
        project_payload = list()

        for org in orgs:
            org_payload.append({
                "org_id": org.org_id,
                "org_name": org.org_name,
            })
            projects = Projects.objects.filter(organization=org.pk)

            for project in projects:
                project_payload.append({
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "org": org.org_id,
                })

        context = {
            "full_name": user.get_full_name,
            "organizations": org_payload,
            "projects": project_payload,
        }
        
        response = render(request, 'frontend/dashboard.html', context)
        return response
