from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from error_logger.models import VerboseLog

from utility.token_manager import protected, decode_token
from utility.helper import get_user_object, get_common_view_payload


class VerboseView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        verbose_logs = VerboseLog.objects.all()

        context = get_common_view_payload(user, "Verbose Log")
        context["verbose_logs"] = verbose_logs
        context["total_logs"] = VerboseLog.objects.all().count()
        context["current"] = len(verbose_logs)
        context["verbose_titles"] = ["#", "User",
                                     "Project Name", "Description", "Origin", "Logged on"]
        
        return render(request, 'frontend/log.html', context)
