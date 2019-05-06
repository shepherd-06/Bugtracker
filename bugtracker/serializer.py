from rest_framework import serializers

from bugtracker.models import *


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectToken
        fields = ('project', 'token', 'refresh_token', 'time_to_live')

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'name', 'password')
#
#     def create(self, validated_data):
#         user = User.objects.create(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#     def validate_email(self, value):
#         if not email_is_valid(value):
#             raise serializers.ValidationError('Please use a different email address provider.')
#
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError('Email already in use, please use a different email address.')
#
#         return value
