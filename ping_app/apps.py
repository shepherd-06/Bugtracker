from django.apps import AppConfig


class PingAppConfig(AppConfig):
    name = 'ping_app'
    
    def ready(self):
        from ping_app.cron_job import start
        start()
