from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from team.models import Team
from projects.models import Projects
from token_manager.models import ProjectToken
from utility.helper import (get_error_count_of_a_project, get_project_object,
                            get_project_token_by_project_id, get_user_object,
                            get_verbose_count_of_a_project, set_cookie, get_common_view_payload)
from utility.token_manager import decode_token, protected


class ProjectView(View):

    @protected
    def get(self, request, project_id: str):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        project = get_project_object(project_id)
        if project is None:
            # TODO: handle error here.
            return JsonResponse({
                "hello": "world",
            }, status=404)

        project_token = get_project_token_by_project_id(project.pk)
        
        context = get_common_view_payload(user, project.project_name)
        context["project_object"] = project
        context["project_token"] = project_token
        context["error_count"] = get_error_count_of_a_project(
            project.project_id)
        context["verbose_count"] = get_verbose_count_of_a_project(project.project_id)

        response = render(request, 'frontend/project.html', context)
        return response
