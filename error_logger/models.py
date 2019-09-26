from django.db import models
from user.models import CustomUser
from projects.models import Projects

# Create your models here.


class ErrorLog(models.Model):
    error_name = models.CharField(max_length=50)
    error_description = models.TextField(max_length=500)
    point_of_origin = models.CharField(max_length=100)
    logged_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ManyToManyField(
        CustomUser, related_name="resolver", blank=True)
    warning_level = models.IntegerField(default=0)
    reference_project = models.ForeignKey(
        Projects, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ["logged_on"]
        verbose_name_plural = "ErrorLog"

    def __str__(self):
        return self.error_name


class VerboseLog(models.Model):
    log_description = models.TextField(max_length=1000, blank=True, null=True)
    point_of_origin = models.CharField(max_length=100)
    logged_on = models.DateTimeField(auto_now_add=True)
    reference_project = models.ForeignKey(Projects, 
                                          on_delete=models.PROTECT,
                                          blank=True, null=True)

    def __str__(self):
        return self.log_title

    class Meta:
        verbose_name_plural = "VerboseLogs"
