from rest_framework import serializers
from ..model.shared_file_model import SharedVaultFile


class ShareFileSerializer(serializers.Serializer):

    file_id = serializers.IntegerField()

    recipient = serializers.CharField()

    encrypted_key = serializers.CharField()

class SharedFileListSerializer(
    serializers.ModelSerializer
):

    sender = serializers.CharField(
        source="sender.username"
    )

    filename = serializers.CharField(
        source="file.original_name"
    )

    # file_id = serializers.IntegerField(
    #     source="file.id"
    # )

    size = serializers.IntegerField(
        source="file.file_size"
    )

    mime_type = serializers.CharField(
        source="file.mime_type"
    )

    class Meta:

        model = SharedVaultFile

        fields = [

            "id",

            "filename",

            "sender",

            "size",

            "mime_type",

            "shared_at"

        ]

