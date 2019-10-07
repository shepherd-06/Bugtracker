from django.db import models
from user.models import CustomUser
from uuid import uuid4
from django.utils import timezone

# Create your models here.


class Team(models.Model):
    team_id = models.CharField(unique=True, max_length=12)
    team_name = models.CharField(max_length=30)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(CustomUser, related_name="team_members")
    team_admins = models.ManyToManyField(CustomUser, related_name="team_admins")

    class Meta:
        verbose_name_plural = "Team"

    def __str__(self):
        return "{}".format(self.team_name)
