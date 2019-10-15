from rest_framework.serializers import ModelSerializer
from team.models import Team


class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ("team_id", "team_name", "created_by")
