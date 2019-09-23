from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_406_NOT_ACCEPTABLE
from django.http import JsonResponse
from utility.helper import get_user_object
from organization.serializer import OrgSerializer
from uuid import uuid4
from organization.models import Organization


class Org(APIView):
    
    # TODO: add access token here from JWT

    required_parameters = ("org_name")

    def post(self, request):
        data = request.data
        user = get_user_object(username=request.user.username)

        for field in self.required_parameters:
            if field not in data:
                return JsonResponse({
                    "message": "Missing mandatory parameter, {field}",
                    "status": HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)

        data["created_by"]: user.pk
        data["org_id"] = str(uuid4())[:12]

        org_serializer = OrgSerializer(data=data)
        if org_serializer.is_valid():
            try:
                org_obj = org_serializer.save()
                return JsonResponse({
                    "message": "A new organization, [ {} ] has been created".format(org_obj.org_name),
                    "org_id": org_obj.org_id,
                    "org_name": org_obj.org_name,
                    "created_by": org_obj.created_by.email,
                    "created_at": org_obj.created_at,
                    "updated_at": org_obj.updated_at,
                    "status": HTTP_201_CREATED,
                }, status=HTTP_201_CREATED)
            except Exception:
                Organization.objects.filter(org_id=org_obj.org_id).delete()
                return JsonResponse({
                    "message": "An error occurred! {}".format(org_serializer.errors),
                    "status": HTTP_400_BAD_REQUEST
                }, status=HTTP_400_BAD_REQUEST)
        else:
            Organization.objects.filter(org_id=org_obj.org_id).delete()
            return JsonResponse({
                "message": "An error occurred! {}".format(org_serializer.errors),
                "status": HTTP_406_NOT_ACCEPTABLE
            }, status=HTTP_406_NOT_ACCEPTABLE)
