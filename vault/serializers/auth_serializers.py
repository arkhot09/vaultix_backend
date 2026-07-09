from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField()
    vault_salt = serializers.CharField()
    vault_verifier = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    latitude = serializers.FloatField(
        required=False,
        allow_null=True
    )

    longitude = serializers.FloatField(
        required=False,
        allow_null=True
    )


class StorePrivateKeySerializer(serializers.Serializer):
    ciphertext = serializers.CharField()
    iv = serializers.CharField()

class VerifyTwoFactorSerializer(
    serializers.Serializer
):
    code = serializers.CharField(max_length = 6)

class VerifyLoginOTPSerializer(serializers.Serializer):
    login_token = serializers.CharField()
    otp = serializers.CharField(max_length = 6)
