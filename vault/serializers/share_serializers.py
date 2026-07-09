from rest_framework import serializers


class ShareEntrySerializer(serializers.Serializer):
    entry_id = serializers.IntegerField()

    recipient = serializers.CharField()

    enc_sym_key = serializers.CharField()

    ciphertext = serializers.CharField()

    iv = serializers.CharField()

    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True
    )


