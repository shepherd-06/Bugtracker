from django.db import models
from user.models import CustomUser
from uuid import uuid4
from django.utils import timezone

# Create your models here.


class Organization(models.Model):
    org_id = models.CharField(unique=True, max_length=12)
    org_name = models.CharField(max_length=30)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(CustomUser, related_name="members")
    org_admins = models.ManyToManyField(CustomUser, related_name="admins")

    class Meta:
        verbose_name_plural = "Organization"

    def __str__(self):
        return "{}".format(self.org_name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.org_id = str(uuid4())[:12]
        else:
            self.modified_on = timezone.now()
        super().save(*args, **kwargs)
