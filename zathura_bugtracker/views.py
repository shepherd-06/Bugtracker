from django.http import HttpResponse
from rest_framework.views import APIView

class Index(APIView):
    
    def get(self, request):
        content = "Hello World.\nThis is the index page of Bugtracker.\nRunning on Pre-Alpha mode"
        return HttpResponse(content, status=200)