from django.db import models
from datetime import datetime
from uuid import uuid4
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


class Errors(models.Model):
    _id = models.UUIDField(default=uuid4(), primary_key=True)
    error_name = models.CharField(max_length=50, null=False)
    error_description = models.TextField(max_length=500, null=False)
    point_of_origin = models.CharField(null=True, default=None, max_length=30)
    logged_at = models.DateTimeField(default=timezone.now())
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(default=None)
    warning_level = models.IntegerField(default=3, null=True, blank=True)


class Logs(models.Model):
    _id = models.UUIDField(default=uuid4(), primary_key=True)
    logs = models.TextField(max_length=1000, null=False)
    logged_at = models.DateTimeField(default=timezone.now())
