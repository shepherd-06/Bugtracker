from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from organization.models import Organization
from projects.models import Projects
from token_manager.models import ProjectToken
from utility.helper import (get_error_count_of_a_project, get_project_object,
                            get_project_token_by_project_id, get_user_object,
                            get_verbose_count_of_a_project, set_cookie)
from utility.token_manager import decode_token, protected


class Project(View):

    @protected
    def get(self, request, project_id):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        project = get_project_object(project_id)
        if project_id is None:
            # TODO: handle error here.
            return JsonResponse({
                "hello": "world",
            }, status=404)

        orgs = Organization.objects.filter(members__pk=user.pk)

        org_payload = list()
        project_payload = list()
        project_object = None

        for org in orgs:
            org_payload.append({
                "org_id": org.org_id,
                "org_name": org.org_name,
            })
            projects = Projects.objects.filter(organization=org.pk)

            for project in projects:
                if project.project_id == project_id:
                    project_object = project
                project_payload.append({
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "org": org.org_id,
                })

        project_token = get_project_token_by_project_id(project_object.pk)

        context = {
            "page_title": project_object.project_name,
            "full_name": user.get_full_name,
            "organizations": org_payload,
            "projects": project_payload,
            "project_object": project_object,
            "project_token": project_token,
            "error_count": get_error_count_of_a_project(project_object.project_id),
            "verbose_count": get_verbose_count_of_a_project(project_object.project_id),
        }

        response = render(request, 'frontend/project.html', context)
        return response
