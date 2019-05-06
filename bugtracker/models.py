from uuid import uuid4

from django.db import models
from django.utils import timezone


# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(unique=True, primary_key=True)
    user_name = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    is_admin = models.BooleanField(default=False)
    user_email = models.EmailField(unique=True)
    user_mobile = models.CharField(unique=True, max_length=20)


class Projects(models.Model):
    _id = models.UUIDField(default=uuid4(), primary_key=True)
    project_id = models.UUIDField(unique=True)
    project_name = models.CharField(max_length=30)
    project_description = models.TextField(max_length=500, null=True, blank=True, default=None)
    registered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    registered_at = models.DateTimeField(default=timezone.now())
    # updated_by = models.ManyToManyField(User, blank=True, default=None)
    updated_at = models.DateTimeField(blank=True)


class Errors(models.Model):
    _id = models.UUIDField(default=uuid4(), primary_key=True)
    error_name = models.CharField(max_length=50, null=False)
    error_description = models.TextField(max_length=500, null=False)
    point_of_origin = models.CharField(null=True, default=None, max_length=30)
    logged_at = models.DateTimeField(default=timezone.now())
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(default=None)
    resolved_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, default=None)
    warning_level = models.IntegerField(default=3, null=True, blank=True)
    reference_project = models.ManyToManyField(Projects, blank=True, default=None)

    class Meta:
        get_latest_by = ['-logged_at']
        ordering = ['-logged_at']


class Logs(models.Model):
    _id = models.UUIDField(default=uuid4(), primary_key=True)
    log_title = models.CharField(max_length=30, null=True, blank=True, default=None)
    logs = models.TextField(max_length=1000, null=False)
    logged_at = models.DateTimeField(default=timezone.now())
    reference_project = models.ManyToManyField(Projects, blank=True, default=None)
