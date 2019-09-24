from rest_framework.serializers import ModelSerializer
from error_logger.models import ErrorLog

class ErrorLoggerSerializer(ModelSerializer):
    
    class Meta:
        model = ErrorLog
        fields = "__all__"