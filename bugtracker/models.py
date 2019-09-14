from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from uuid import uuid4
# Create your models here.
from bugtracker.model_managers.managers import MyUserManager


class User(AbstractUser):
    user_id = models.UUIDField(unique=True, primary_key=True)
    full_name = models.CharField(max_length=20, blank=False, null=False)
    username = models.CharField(unique=True, max_length=12)
    email = models.EmailField(unique=True)
    updated_at = models.DateTimeField(default=timezone.now())
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']

    class Meta:
        verbose_name_plural = "User"
        # Latest by priority descending, order_date ascending.
        get_latest_by = ['created_at']
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return "{} - {}".format(self.full_name, self.email)


class Organisation(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    org_id = models.UUIDField(unique=True, blank=True)
    org_name = models.CharField(max_length=20, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    class Meta:
        verbose_name_plural = "Organisation"
        default_permissions = ('add', 'change', 'delete', 'view')

    def __str__(self):
        return "{}".format(self.org_name)

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = uuid4()
            self.org_id = uuid4()
            self.created_at = timezone.now()
            self.updated_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class UserToOrg(models.Model):
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_added = models.DateTimeField(blank=True)

    class Meta:
        verbose_name_plural = "User & Org connecting Table"

    def __str__(self):
        return "{} --- {}".format(self.user, self.organization)

    def save(self, *args, **kwargs):
        self.user_added = timezone.now()
        super().save(*args, **kwargs)


class UserToken(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    authorized_user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, blank=True)
    refresh_token = models.UUIDField(unique=True, blank=True)
    generated_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(
        blank=True, verbose_name="First entry time")
    time_to_live = models.IntegerField(default=864000)

    class Meta:
        verbose_name_plural = "User Access Token management"

    def __str__(self):
        return "For {} || Generated At: {}".format(self.authorized_user, self.generated_at)

    def save(self, *args, **kwargs):
        if self._id is None:
            self.generated_at = timezone.now()
            self.updated_at = timezone.now()
            self.created_at = timezone.now()
            self.refresh_token = uuid4()
            self.token = uuid4()
            self._id = uuid4()
        else:
            self.generated_at = timezone.now()
            self.updated_at = timezone.now()
            self.refresh_token = uuid4()
            self.token = uuid4()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Projects(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    project_id = models.UUIDField(unique=True, blank=True)
    project_name = models.CharField(max_length=30)
    project_description = models.TextField(max_length=500, null=True, blank=True,
                                           default=None)
    registered_by = models.ForeignKey(User, on_delete=models.PROTECT)
    registered_at = models.DateTimeField(blank=True)
    organization = models.ForeignKey(Organisation, on_delete=models.PROTECT)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name_plural = "All Project name"
        default_permissions = ('add', 'change', 'delete', 'view')

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = uuid4()
            self.registered_at = timezone.now()
            self.project_id = uuid4()
        if len(self.project_name) > 30 or len(self.project_name) == 0:
            raise ValidationError("Project name field is mandatory. Length of Project name cannot be more than 30 "
                                  "characters")
        if self.project_description is not None and len(self.project_description) > 500:
            raise ValidationError(
                "Project description can be null, but cannot exceed 500 characters, if given")
        super().save(*args, **kwargs)  # Call the "real" save() method.


class ProjectUpdate(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        title = "Project name: {}, updated_by: {}".format(self.project.project_name,
                                                          self.updated_by.email)
        return title

    class Meta:
        verbose_name_plural = "Project & User connecting Table"
        default_permissions = ('add', 'change', 'delete', 'view')

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class ProjectToken(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    project = models.OneToOneField(
        Projects, on_delete=models.CASCADE, unique=True)
    token = models.UUIDField(unique=True, blank=True)
    refresh_token = models.UUIDField(unique=True, blank=True)
    generated_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    time_to_live = models.IntegerField(default=864000)

    def __str__(self):
        return "For {} || Generated At: {}".format(self.project, self.generated_at)

    class Meta:
        verbose_name_plural = "Project Access Token"

    def save(self, *args, **kwargs):
        print(**kwargs)
        print(*args)
        if self._id is None:
            self._id = uuid4()
            self.generated_at = timezone.now()

        self.token = uuid4()
        self.refresh_token = uuid4()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Errors(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    error_name = models.CharField(max_length=50, null=False)
    error_description = models.TextField(max_length=500, null=False)
    point_of_origin = models.CharField(max_length=100, null=False)
    logged_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    is_resolved = models.BooleanField(default=False)
    issued_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, default=None, null=True)
    warning_level = models.IntegerField(default=-1, null=True, blank=True)
    reference_project = models.ForeignKey(
        Projects, on_delete=models.PROTECT, default=None, null=True)

    class Meta:
        ordering = ["logged_at"]
        verbose_name_plural = "All Error logs"

    def __str__(self):
        return self.error_name

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = uuid4()
            self.logged_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class ErrorStatus(models.Model):
    error = models.ForeignKey(Errors, on_delete=models.CASCADE)
    resolved_by = models.ForeignKey(User, on_delete=models.PROTECT)
    resolved_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    def __str__(self):
        return "Error name: {}, resolved_by: {}".format(self.error.error_name, self.resolved_by.user_email)

    class Meta:
        verbose_name_plural = "Error User connecting Table"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.resolved_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Logs(models.Model):
    _id = models.UUIDField(primary_key=True, blank=True)
    log_title = models.CharField(
        max_length=30, null=True, blank=True, default=None)
    logs = models.TextField(max_length=1000, null=False)
    logged_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    reference_project = models.ForeignKey(Projects, on_delete=models.PROTECT, blank=True,
                                          default=None, null=True)

    def __str__(self):
        return self.log_title

    class Meta:
        verbose_name_plural = "All debug logs"

    def save(self, *args, **kwargs):
        self._id = uuid4()
        self.logged_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Invitation(models.Model):
    user_email = models.EmailField(unique=True)
    invited_at = models.DateTimeField(blank=True)
    invited_by = models.ForeignKey(User, on_delete=models.PROTECT)
    is_used = models.BooleanField(blank=True)

    def __str__(self):
        return "User: {} | Invited by {}".format(self.user_email, self.invited_by.user_email)

    class Meta:
        verbose_name_plural = "Invitation"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.invited_at = timezone.now()
            self.is_used = False
        super().save(*args, **kwargs)  # Call the "real" save() method.
