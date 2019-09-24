from rest_framework.serializers import ModelSerializer
from token_manager.models import ProjectToken

class TokenSerializer(ModelSerializer):
    class Meta:
        model = ProjectToken
        fields = "__all__"