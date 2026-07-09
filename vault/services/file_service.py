from rest_framework.exceptions import ValidationError
import os

from ..model.file_model import (
    Folder,
    VaultFile
)


class FileService:

    # @staticmethod
    # def create_folder(user,validated_data):
    #     parent = validated_data.get("parent")
    #     if (parent and parent.owner != user):
    #         raise ValidationError("Invalid parent folder.")

    #     exists = Folder.objects.filter(
    #         owner=user,
    #         parent=parent,
    #         name=validated_data["name"]
    #     ).exists()

    #     if exists:

    #         raise ValidationError("Folder already exists.")

    #     return Folder.objects.create(
    #         owner=user,
    #         parent=parent,
    #         name=validated_data["name"]
    #     )

    # @staticmethod
    # def get_folders(user, parent=None):

    #     return Folder.objects.filter(owner=user, parent=parent
    #     ).order_by("name")

    # @staticmethod
    # def rename_folder(
    #     user,
    #     folder_id,
    #     validated_data
    # ):

    #     folder = Folder.objects.get(
    #         id=folder_id,
    #         owner=user
    #     )

    #     duplicate = Folder.objects.filter(
    #         owner=user,
    #         parent=folder.parent,
    #         name=validated_data["name"]
    #     ).exclude(
    #         id=folder.id
    #     ).exists()

    #     if duplicate:
    #         raise ValidationError("Folder already exists.")
    #     folder.name = validated_data["name"]
    #     folder.save()
    #     return folder

    # @staticmethod
    # def delete_folder(
    #     user,
    #     folder_id
    # ):

    #     folder = Folder.objects.get(
    #         id=folder_id,
    #         owner=user
    #     )

    #     folder.delete()

    @staticmethod
    def upload_file(
        user,
        validated_data
    ):

        folder = None

        if validated_data.get("folder"):

            folder = Folder.objects.get(
                id=validated_data["folder"],
                owner=user
            )

        uploaded = validated_data["file"]

        storage_name = uploaded.name

        original_name = validated_data["original_name"]

        filename = uploaded.name

        extension = os.path.splitext(
            filename
        )[1]

        return VaultFile.objects.create(

    owner=user,

    folder=folder,

    filename=storage_name,

    original_name=original_name,

    extension=extension,

    mime_type=uploaded.content_type,

    file_size=uploaded.size,

    encrypted_file=uploaded,

    encrypted_key=validated_data[
        "encrypted_key"
    ].encode(),

    iv=validated_data["iv"],

    algorithm=validated_data["algorithm"]

)
    @staticmethod
       
    def list_files(user, folder=None):

        files = VaultFile.objects.filter(
            owner=user,
            folder=folder
        ).order_by("-created_at")

        return files