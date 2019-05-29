from rest_framework import serializers

from bugtracker.model_managers.models import *


class ProjectTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectToken
        fields = "__all__"


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errors
        fields = ('error_name', 'error_description', 'point_of_origin', 'reference_project')


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUpdate
        fields = "__all__"


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('user_email', 'user_name', 'password', 'is_admin')

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        validated_data['user_id'] = uuid4()
        validated_data['updated_at'] = timezone.now()
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def validate_email(value):
        # if not email_is_valid(value):
        #     raise serializers.ValidationError('Please use a different email address provider.')

        if User.objects.filter(user_email=value).exists():
            raise serializers.ValidationError('Email already in use, please use a different email address.')
        return value
