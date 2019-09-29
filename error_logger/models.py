from django.db import models
from user.models import CustomUser
from projects.models import Projects

# Create your models here.


class ErrorLog(models.Model):
    identifier = models.CharField(
        max_length=50, blank=True, null=True, default="Anonymous", verbose_name="user")
    error_name = models.CharField(max_length=50)
    error_description = models.TextField(max_length=500, verbose_name="description")
    point_of_origin = models.CharField(max_length=100, verbose_name="origin")
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
        verbose_name_plural = "errorLogs"

    def __str__(self):
        return "Error name: {} | Logged on: {}".format(self.error_name, self.logged_on)

    def get_project_name(self):
        return self.reference_project.project_name

    project_name = property(get_project_name)


class VerboseLog(models.Model):
    identifier = models.CharField(
        max_length=50, blank=True, null=True, default="Anonymous", verbose_name="user")
    log_description = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Description")
    point_of_origin = models.CharField(max_length=100, verbose_name="origin")
    logged_on = models.DateTimeField(auto_now_add=True)
    reference_project = models.ForeignKey(Projects,
                                          on_delete=models.PROTECT,
                                          blank=True, null=True)

    def __str__(self):
        return "Origin: {} | Logged on: {}".format(self.point_of_origin, self.logged_on)

    class Meta:
        verbose_name_plural = "verboseLogs"

    def get_project_name(self):
        return self.reference_project.project_name

    project_name = property(get_project_name)
