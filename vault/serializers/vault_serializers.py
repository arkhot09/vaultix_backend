from rest_framework import serializers


class VaultEntrySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    ciphertext = serializers.CharField()
    iv = serializers.CharField()
    health = serializers.DictField(required=False)


class UpdateVaultEntrySerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        required=False
    )

    ciphertext = serializers.CharField()

    iv = serializers.CharField()