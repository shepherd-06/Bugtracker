from uuid import uuid4

from django.http import JsonResponse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_406_NOT_ACCEPTABLE)
from django.views import View

from organization.models import Organization
from organization.serializer import OrgSerializer
from utility.helper import get_user_object
from utility.token_manager import decode_token, protected


class Org(View):

    # TODO: take members email addresses in a list, as parameter.
    # TODO: get the user object via email address and add them as member.
    # TODO: Do same for admins later

    required_parameters = ("org_name",)

    @protected
    def post(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        for field in self.required_parameters:
            if field not in request.POST:
                return JsonResponse({
                    "message": "Missing mandatory parameter, {}".format(field),
                    "status": HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)
        data = {
            "org_name": request.POST["org_name"],
        }
        data["created_by"] = user.pk
        data["org_id"] = str(uuid4())[:12]

        org_serializer = OrgSerializer(data=data)
        if org_serializer.is_valid():
            try:
                org_obj = org_serializer.save()
                org_obj.members.add(user)
                org_obj.org_admins.add(user)
                org_obj.save()

                return JsonResponse({
                    "message": "A new organization, [ {} ] has been created".format(org_obj.org_name),
                    "org_id": org_obj.org_id,
                    "org_name": org_obj.org_name,
                    "created_by": org_obj.created_by.email,
                    "created_on": org_obj.created_on,
                    "status": HTTP_201_CREATED,
                }, status=HTTP_201_CREATED)
            except Exception as e:
                Organization.objects.filter(org_id=org_obj.org_id).delete()
                return JsonResponse({
                    "message": "An error occurred! {}".format(e),
                    "status": HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                "message": "An error occurred! {}".format(org_serializer.errors),
                "status": HTTP_406_NOT_ACCEPTABLE
            }, status=HTTP_406_NOT_ACCEPTABLE)

    @protected
    def get(self, request):
        """
        send the organizations user is part of. 
        store those values in cookies.
        """
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])

        orgs = Organization.objects.filter(members__pk=user.pk)
        
        for org in orgs:
            print(org.org_name)
            
        return JsonResponse({
            "hello": "world",
        })