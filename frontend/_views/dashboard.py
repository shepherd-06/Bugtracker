from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from utility.token_manager import decode_token, protected
from utility.helper import get_user_object, set_cookie
from team.models import Team
from projects.models import Projects
# Create your views here.


class Dashboard(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        teams = Team.objects.filter(members__pk=user.pk)
        
        team_payload = list()
        project_payload = list()

        for team in teams:
            team_payload.append({
                "team_id": team.team_id,
                "team_name": team.team_name,
            })
            projects = Projects.objects.filter(team=team.pk)

            for project in projects:
                project_payload.append({
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "team": team.team_id,
                })

        context = {
            "full_name": user.get_full_name,
            "teams": team_payload,
            "projects": project_payload,
        }
        
        response = render(request, 'frontend/dashboard.html', context)
        return response
