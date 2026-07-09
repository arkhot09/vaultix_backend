from rest_framework import serializers

from ..model.file_model import Folder


class FolderSerializer(serializers.ModelSerializer):

    class Meta:

        model = Folder

        fields = [
            "id",
            "name",
            "parent",
            "created_at",
            "updated_at"
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]


class FolderRenameSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=255
    )

class UploadFileSerializer(
    serializers.Serializer
):

    folder = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    iv = serializers.CharField()

    file = serializers.FileField()

class UploadFileSerializer(serializers.Serializer):

    folder = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    original_name = serializers.CharField()

    iv = serializers.CharField()

    encrypted_key = serializers.CharField()

    algorithm = serializers.CharField()

    file = serializers.FileField()
