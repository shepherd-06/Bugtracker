from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from ping_app.serializer import WebSerializer
from utility.helper import get_user_object


# Create your views here.
class Ping(APIView):

    permission_classes = (IsAuthenticated,)

    """
    structure
    urls = [
        {
            "url": "https://www.google.com",
            "type": "get",
        }
    ]
    """

    required_field = ("urls",)
    child_field = ("url", "type")

    def post(self, request):
        data = request.data
        user = get_user_object(username=request.user.username)
        for field in self.required_field:
            if field not in data:
                return JsonResponse({
                    "status": False,
                    "message": "Required parameter missing. {} is required".format(field),
                }, status=HTTP_400_BAD_REQUEST)

        urls = data["urls"]  # it's a list
        
        if not isinstance(urls, list):
            return JsonResponse({
                "status": False,
                "message": "urls is supposed to be a list.",
            }, status=HTTP_400_BAD_REQUEST)
            
        final_tally = []
        counter = 0

        for url in urls:
            for field in self.child_field:
                if field not in url:
                    return JsonResponse({
                        "status": False,
                        "message": "Required parameter missing. {} is required".format(field),
                    }, status=HTTP_400_BAD_REQUEST)
            url["status"] = 0
            url["verbose_status"] = "Initializing"
            url["created_by"] = user.pk

            serializer = WebSerializer(data=url)
            
            if serializer.is_valid():
                serializer.save()
                final_tally.append({
                    "url": url["url"],
                    "status": True,
                    "message": "success" 
                })
                counter += 1
            else:
                message = serializer.errors
                final_tally.append({
                    "url": url["url"],
                    "status": False,
                    "message": message,
                })
        
        reply = {
            "status": True,
            "message": "Success: {} urls. Failed: {}".format(counter, (len(data["urls"]) - counter)),
            "description": final_tally,
        }
        return JsonResponse(reply, status=HTTP_200_OK)
