from uuid import uuid4

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

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
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email already in use, please use a different email address.')
        return value

    def validate_password(self, password):
        """Validates that a password is as least 7 characters long and has at least
        1 digit and 1 letter.
        """
        min_length = 7

        if len(password) < min_length:
            raise ValidationError(_('Password must be at least {0} characters '
                                    'long.').format(min_length))

        # check for digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least 1 digit.'))

        # check for letter
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _('Password must contain at least 1 letter.'))

        return password
