from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_active', 'joined_date', 'is_staff')


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh_token = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh_token'] = str(refresh_token)
        data['access_token'] = str(refresh_token.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UserSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        max_length=128
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())], max_length=20
    )
    password = serializers.CharField(min_length=12, max_length=128, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'is_active', 'joined_date')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
