import requests
from ping_app.models import WebStatus
from apscheduler.schedulers.background import BackgroundScheduler
import urllib3

# HTTP_METHODS = (
#     ("GET", "1"),
#     ("HEAD", "2"),
#     ("POST", "3"),
#     ("PUT", "4"),
#     ("DELETE", "5"),
#     ("CONNECT", "6"),
#     ("OPTIONS", "7"),
#     ("TRACE", "8")
# )

def jobs():
    all_objects = WebStatus.objects.all()

    for obj in all_objects:
        try:
            if obj.request_type == "2":
                response = requests.head(obj.url)
            # elif obj.request_type == "3":
            #     response = requests.post(obj.url)
            elif obj.request_type == "4":
                response = requests.put(obj.url)
            elif obj.request_type == "5":
                response = requests.delete(obj.url)
            elif obj.request_type == "6":
                response = requests.options(obj.url)
            else:
                response = requests.get(obj.url)

            status = response.status_code
            obj.status = status
            obj.verbose_status = str(status)
            obj.save()
        except Exception:
            obj.status = -1
            obj.verbose_status = "Connection Refused"
            obj.save()
        


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobs, 'interval', minutes=5)
    scheduler.start()
