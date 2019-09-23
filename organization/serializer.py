from organization.models import Organization
from rest_framework.serializers import ModelSerializer

class OrgSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"