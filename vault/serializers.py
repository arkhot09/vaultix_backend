from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import VaultEntry, SharedEntry, Profile

# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField(required=False)
#     master_password = serializers.CharField(write_only=True)


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Hash password before saving
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

class VaultEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultEntry
        fields = ['id', 'site', 'login', 'ciphertext', 'iv', 'salt', 'created_at']
        read_only_fields = ['id','created_at']

class SharedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedEntry
        fields = ['id','entry','sender','recipient','enc_sym_key','iv','ciphertext','created_at']
