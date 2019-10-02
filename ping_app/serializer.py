from rest_framework.serializers import ModelSerializer
from ping_app.models import WebStatus


class WebSerializer(ModelSerializer):

    class Meta:
        model = WebStatus
        fields = "__all__"

