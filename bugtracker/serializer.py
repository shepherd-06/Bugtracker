from rest_framework import serializers

from bugtracker.models import *


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectToken
        fields = ('project', 'token', 'refresh_token', 'time_to_live')


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errors
        fields = ('error_name', 'error_description', 'point_of_origin', 'reference_project')


class UserRegistrationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('user_email', 'user_name', 'password', 'is_admin')

    def create(self, validated_data):
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
