from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime

from team.models import Team
from utility.helper import get_user_object, get_common_view_payload
from utility.token_manager import decode_token, protected


class ProfileView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        
        print("----------------------------------")
        print(user.created_on)
        print(datetime.timestamp(user.created_on))
        print("----------------------------------")
        
        user.created_on = datetime.timestamp(user.created_on)
        user.modified_on = datetime.timestamp(user.modified_on)
        

        teams = Team.objects.filter(members__pk=user.pk)
        team_payload = list()
        for team in teams:
            team_payload.append({
                "team_id": team.team_id,
                "team_name": team.team_name,
                "member": True,
                "admin": True if Team.objects.filter(
                    team_admins__pk=user.pk) else False
            })
            
        
        context = get_common_view_payload(user, user.get_full_name)
        context["user"] = user
        context["team_payload"] = team_payload
        context["total_team"] = len(team_payload)
 
        return render(request, 'frontend/profile.html', context)
