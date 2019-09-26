from rest_framework.serializers import ModelSerializer
from error_logger.models import ErrorLog, VerboseLog


class ErrorLoggerSerializer(ModelSerializer):

    class Meta:
        model = ErrorLog
        fields = "__all__"


class VerboseLogSerializer(ModelSerializer):

    class Meta:
        model = VerboseLog
        fields = "__all__"
