from django.db import models
from projects.models import Projects


class ProjectToken(models.Model):
    project = models.OneToOneField(Projects, on_delete=models.CASCADE)
    token = models.CharField(unique=True, max_length=36)
    generated_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_access = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "For {} || Generated At: {}".format(self.project, self.generated_on)

    class Meta:
        verbose_name_plural = "ProjectToken"
