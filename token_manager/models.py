from django.db import models
from projects.models import Projects


class ProjectToken(models.Model):
    project = models.OneToOneField(
        Projects, on_delete=models.CASCADE, unique=True)
    token = models.UUIDField(unique=True, blank=True)
    refresh_token = models.UUIDField(unique=True, blank=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "For {} || Generated At: {}".format(self.project, self.generated_on)

    class Meta:
        verbose_name_plural = "ProjectToken"
