import requests
from ping_app.models import WebStatus
from apscheduler.schedulers.background import BackgroundScheduler
import urllib3


def jobs():
    """
    PING only supports GET, OPTIONS and HEAD method.
    """
    all_objects = WebStatus.objects.all()

    for obj in all_objects:
        try:
            if obj.request_type == "2":
                response = requests.head(obj.url)
            elif obj.request_type == "3":
                response = requests.options(obj.url)
            else:
                response = requests.get(obj.url)

            status = response.status_code
            obj.status = status
            obj.verbose_status = requests.status_codes._codes[status][0]
            obj.save()
        except Exception:
            obj.status = -1
            obj.verbose_status = "Connection Refused"
            obj.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobs, 'interval', minutes=5)
    scheduler.start()
