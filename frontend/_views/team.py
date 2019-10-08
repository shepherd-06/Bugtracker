from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from team.models import Team
from projects.models import Projects
from token_manager.models import ProjectToken
from utility.helper import get_team_object, get_user_object, get_common_view_payload
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
        
        context = get_common_view_payload(user, team.team_name)
        context["current_team"] = team
        return render(request, 'frontend/team.html', context)
        
