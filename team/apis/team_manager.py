from uuid import uuid4

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse
from django.views import View
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_406_NOT_ACCEPTABLE)

from team.models import Team
from team.serializer import TeamSerializer
from utility.helper import get_user_object
from utility.token_manager import decode_token, protected


class TeamManager(View):

    # TODO: take members email addresses in a list, as parameter.
    # TODO: get the user object via email address and add them as member.
    # TODO: Do same for admins later

    required_parameters = ("team_name",)

    @protected
    def post(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        for field in self.required_parameters:
            if field not in request.POST:
                message = "Missing mandatory parameter, {}".format(field)
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?message={}&status={}".format(message, True),
                )
        data = {
            "team_name": request.POST["team_name"],
        }
        data["created_by"] = user.pk
        data["team_id"] = str(uuid4())[:12]

        team_serializer = TeamSerializer(data=data)
        if team_serializer.is_valid():
            try:
                team_obj = team_serializer.save()
                team_obj.members.add(user)
                team_obj.team_admins.add(user)
                team_obj.save()

                message = "Success"
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?message={}&status={}".format(message, True),
                )
            except Exception as e:
                Team.objects.filter(team_id=team_obj.team_id).delete()
                print(
                    "An Error occurred while creating a new team. Error message: {}".format(e))
                message = "An error occurred!"
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?message={}&status={}".format(message, False),
                )
        else:
            print(
                "An Error occurred while creating a new team. Error message: {}".format(team_serializer.errors))
            message = "An error occurred!"
            return HttpResponseRedirect(
                reverse("dashboard") +
                "?message={}&status={}".format(message, False),
            )
