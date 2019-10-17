from uuid import uuid4

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_406_NOT_ACCEPTABLE)
from django.views import View

from ping_app.serializer import WebSerializer
from utility.helper import get_user_object
from utility.token_manager import decode_token, protected


class Ping(View):

    required_parameters = ("url", "type")

    @protected
    def post(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        for field in self.required_parameters:
            if field not in request.POST:
                message = "Missing mandatory parameter, {}".format(field)
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?message={}&status={}".format(message, False),
                )

        data = {
            "url": request.POST["url"],
            "request_type": request.POST["type"],
        }
        data["status"] = 0
        data["verbose_status"] = "Initializing"
        data["created_by"] = user.pk

        web_serializer = WebSerializer(data=data)
        if web_serializer.is_valid():
            try:
                web_serializer.save()
                message = "successfully added a new url"
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?ping_message={}".format(message),
                )
            except Exception:
                message = "An error occurred! "
                return HttpResponseRedirect(
                    reverse("dashboard") +
                    "?ping_message={}&status={}".format(message, False),
                )
        else:
            message = "An error occurred! {}".format(web_serializer.errors)
            return HttpResponseRedirect(
                reverse("dashboard") +
                "?ping_message={}&status={}".format(message, False),
            )
