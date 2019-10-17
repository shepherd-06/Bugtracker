from uuid import uuid4

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_406_NOT_ACCEPTABLE)

from token_manager.serializer import TokenSerializer
from utility.helper import (get_project_object,
                            get_project_token_by_project_id, get_user_object)
from utility.token_manager import decode_token, protected


class ProjectToken(View):

    @protected
    def post(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        # TODO: check if user is an admin to create a project under this org.

        if "project_id" not in request.POST:
            message = "Missing required parameter. {project_id} is required"
            return HttpResponseRedirect(
                reverse("project", args=("None",))+"?message={}&status={}".format(
                    message, False),
            )

        data = {
            "project_id": request.POST["project_id"],
        }

        project_obj = get_project_object(project_id=data["project_id"])
        if project_obj is None:
            message = "Selected project is not found"
            return HttpResponseRedirect(
                reverse("project", args=(request.POST["project_id"],))+"?message={}&status={}".format(
                    message, False),
            )

        project_token_obj = get_project_token_by_project_id(project_obj.pk)
        if project_token_obj is not None:
            message = "Token already generated for this project. One token per project"
            return HttpResponseRedirect(
                reverse("project", args=(request.POST["project_id"],))+"?message={}&status={}".format(
                    message, False),
            )

        data["project"] = project_obj.pk
        data["token"] = str(uuid4())

        project_token_serializer = TokenSerializer(data=data)

        if project_token_serializer.is_valid():
            project_token_obj = project_token_serializer.save()

            if project_token_obj.pk:
                message = "successfully created new project token"
                return HttpResponseRedirect(
                    reverse("project", args=(request.POST["project_id"],))+"?message={}&status={}".format(
                        message, True),
                )
            else:
                message = "Error occurred creating new project token."
                return HttpResponseRedirect(
                    reverse("project", args=(request.POST["project_id"],))+"?message={}&status={}".format(
                        message, False),
                )
        else:
            # Error
            message = "Error occurred creating new project token. {}".format(
                project_token_serializer.errors)
            return HttpResponseRedirect(
                reverse("project", args=(request.POST["project_id"],))+"?message={}&status={}".format(
                    message, False),
            )
