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