from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render

from error_logger.models import ErrorLog

from utility.token_manager import protected, decode_token
from utility.helper import get_user_object, get_common_view_payload

from datetime import datetime


class ErrorLogView(View):

    @protected
    def get(self, request):
        payload = decode_token(request.COOKIES['access_token'])
        user = get_user_object(username=payload["sub"])
        error_logs = ErrorLog.objects.all()
        for logs in error_logs:
            logs.logged_on = datetime.timestamp(logs.logged_on) * 1000
            logs.updated_on = datetime.timestamp(logs.updated_on) * 1000

        context = get_common_view_payload(user, "Error Log")
        context["error_logs"] = error_logs
        context["total_logs"] = ErrorLog.objects.all().count()
        context["current"] = len(error_logs)
        context["titles"] = [
            "#",
            "User",
            "Error Name",
            "Description",
            "Origin",
            "Project",
            "Logged on",
            "Status",
            "Resolved by",
            "Last Updated",
        ]

        return render(request, 'frontend/log.html', context)
