from django.contrib import admin
from error_logger.models import ErrorLog, VerboseLog

# Register your models here.
admin.site.register(ErrorLog)
admin.site.register(VerboseLog)