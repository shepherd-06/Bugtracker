from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

# Create your models here.
from bugtracker.model_managers.managers import MyUserManager


class User(AbstractBaseUser):
    user_id = models.UUIDField(unique=True, primary_key=True)
    user_name = models.CharField(max_length=20, blank=False, null=False)
    user_email = models.EmailField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    class Meta:
        verbose_name_plural = "User"
        # Latest by priority descending, order_date ascending.
        get_latest_by = ['created_at']

    def __str__(self):
        return "{} - {}".format(self.user_name, self.user_email)


class UserToken(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    authorized_user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, blank=True)
    refresh_token = models.UUIDField(unique=True, blank=True)
    generated_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    time_to_live = models.IntegerField(default=864000)

    def __str__(self):
        return "For {} || Generated At: {}".format(self.authorized_user, self.generated_at)

    def save(self, *args, **kwargs):
        self.generated_at = timezone.now()
        self.updated_at = timezone.now()
        self.refresh_token = uuid4()
        self.token = uuid4()
        self._id = uuid4()
        print("Super save method?")
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _do_update(self, *args, **kwargs):
        # Some Business Logic
        self.updated_at = timezone.now()
        super()._do_update(*args, **kwargs)


class Projects(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    project_id = models.UUIDField(unique=True, blank=True)
    project_name = models.CharField(max_length=30)
    project_description = models.TextField(max_length=500, null=True, blank=True,
                                           default=None)
    registered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    registered_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        self.registered_at = timezone.now()
        self.project_id = uuid4()
        self._id = uuid4()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class ProjectUpdate(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        title = "Project name: {}, updated_by: {}".format(self.project.project_name,
                                                          self.updated_by.user_email)
        return title

    class Meta:
        verbose_name_plural = "ProjectUpdate"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _do_update(self, *args, **kwargs):
        # Some Business Logic
        self.updated_at = timezone.now()
        super()._do_update(*args, **kwargs)


class ProjectToken(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, blank=True)
    refresh_token = models.UUIDField(unique=True, blank=True)
    generated_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    time_to_live = models.IntegerField(default=864000)

    def __str__(self):
        return "For {} || Generated At: {}".format(self.project, self.generated_at)

    class Meta:
        verbose_name_plural = "ProjectToken"

    def save(self, *args, **kwargs):
        self._id = uuid4()
        self.token = uuid4()
        self.refresh_token = uuid4()
        self.generated_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _do_update(self, *args, **kwargs):
        # Some Business Logic
        self.updated_at = timezone.now()
        super()._do_update(*args, **kwargs)


class Errors(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    error_name = models.CharField(max_length=50, null=False)
    error_description = models.TextField(max_length=500, null=False)
    point_of_origin = models.CharField(max_length=100, null=False)
    logged_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    is_resolved = models.BooleanField(default=False)
    issued_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, default=None, null=True)
    warning_level = models.IntegerField(default=-1, null=True, blank=True)
    reference_project = models.ForeignKey(Projects, on_delete=models.PROTECT, default=None, null=True)

    class Meta:
        ordering = ["logged_at"]
        verbose_name_plural = "Errors"

    def __str__(self):
        return self.error_name

    def save(self, *args, **kwargs):
        self._id = uuid4()
        self.logged_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _do_update(self, *args, **kwargs):
        # Some Business Logic
        self.updated_at = timezone.now()
        super()._do_update(*args, **kwargs)


class ErrorStatus(models.Model):
    error = models.ForeignKey(Errors, on_delete=models.CASCADE)
    resolved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    resolved_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return "Error name: {}, resolved_by: {}".format(self.error.error_name, self.resolved_by.user_email)

    class Meta:
        verbose_name_plural = "ErrorStatus"

    def save(self, *args, **kwargs):
        self.resolved_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Logs(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    log_title = models.CharField(max_length=30, null=True, blank=True, default=None)
    logs = models.TextField(max_length=1000, null=False)
    logged_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    reference_project = models.ForeignKey(Projects, on_delete=models.PROTECT, blank=True,
                                          default=None, null=True)

    def __str__(self):
        return self.log_title

    class Meta:
        verbose_name_plural = "Logs"

    def save(self, *args, **kwargs):
        self._id = uuid4()
        self.logged_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def _do_update(self, *args, **kwargs):
        # Some Business Logic
        self.updated_at = timezone.now()
        super()._do_update(*args, **kwargs)
