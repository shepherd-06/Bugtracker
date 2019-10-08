from django.db import models
from user.models import CustomUser


HTTP_METHODS = (
    ("1", "GET"),
    ("2", "HEAD"),
    ("3", "OPTIONS")
)


class WebStatus(models.Model):
    url = models.CharField(max_length=1000, verbose_name="URL")
    request_type = models.CharField(max_length=1, choices=HTTP_METHODS, default="7")
    status = models.IntegerField(verbose_name="HTTP Status")
    verbose_status = models.CharField(max_length=50, verbose_name="Descrption")
    last_checked = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Website Status"
