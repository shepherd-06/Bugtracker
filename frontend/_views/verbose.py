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
        
        context = get_common_view_payload(user, "Error Log")
        context["verbose_logs"] = verbose_logs
        context["total_logs"] = VerboseLog.objects.all().count()
        context["current"] = len(verbose_logs)
        
        return render(request, 'frontend/verbose_log.html', context)