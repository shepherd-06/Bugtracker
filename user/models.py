from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """
    Customized User Model
    """
    email = models.EmailField(blank=True, null=True,
                              max_length=256, unique=True)
    mobile_no = models.CharField(
        max_length=20, blank=True, null=True, unique=True)
    verification_code = models.CharField(max_length=8)
    timezone = models.CharField(max_length=10, blank=True, null=True)
    pin_verified = models.BooleanField(default=False)
    modified_on = models.DateTimeField('date modified', auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "CustomUser"

    def __str__(self):
        if not self.is_anonymous:
            if self.mobile_no is not None:
                return str(self.mobile_no)
            else:
                return str(self.email)
        else:
            return "Anon"

    @property
    def get_full_name(self):
        full_name = super().get_full_name()
        if len(full_name) == 0:
            return self.email
        return full_name

    def get_all_permissions(self, obj=None):
        return super().get_all_permissions(obj=obj)
