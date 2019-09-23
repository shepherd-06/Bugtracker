from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from uuid import uuid4

from user.models import CustomUser


class UserSerializer(ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def validate_email(value):
        # if not email_is_valid(value):
        #     raise serializers.ValidationError('Please use a different email address provider.')

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already in use, please use a different email address.')
        return value
