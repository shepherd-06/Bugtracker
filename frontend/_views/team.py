from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from projects.models import Projects
from team.models import Team
from token_manager.models import ProjectToken
from utility.helper import (get_common_view_payload, get_team_object,
                            get_user_object)
from utility.token_manager import decode_token, protected


class TeamView(View):

    @protected
    def get(self, request, team_id: str):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        team = get_team_object(team_id)
        if team is None:
            # TODO: handle error here.
            return JsonResponse({
                "hello": "world",
            }, status=404)
            
        team.created_on = datetime.timestamp(team.created_on) * 1000
        team.modified_on = datetime.timestamp(team.modified_on) * 1000

        is_member = True if Team.objects.filter(members__pk=user.pk) else False
        is_admin = True if Team.objects.filter(
            team_admins__pk=user.pk) else False
        
        projects = Projects.objects.filter(team=team.pk)

        context = get_common_view_payload(user, team.team_name)
        context["current_team"] = team
        context["is_member"] = is_member
        context["is_admin"] = is_admin
        context["admins"] = team.team_admins.all()
        context["members"] = team.members.all()
        context["projects"] = projects
        context["total_projects"] = len(projects)
        context["total_members"] = len(team.members.all())
        context["total_admins"] = len(team.team_admins.all())

        return render(request, 'frontend/team.html', context)
