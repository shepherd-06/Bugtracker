from django.db import models
from team.models import Team
from uuid import uuid4


class Projects(models.Model):
    project_id = models.CharField(unique=True, max_length=12)
    project_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name_plural = "Projects"
        default_permissions = ('add', 'change', 'delete', 'view')
