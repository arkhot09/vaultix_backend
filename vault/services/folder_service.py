from ..model.file_model import Folder


class FolderService:

    @staticmethod
    def create_folder(user, validated_data):

        return Folder.objects.create(

            owner=user,

            parent=validated_data.get("parent"),

            name=validated_data["name"]

        )


    @staticmethod
    def get_root_folders(user):

        return Folder.objects.filter(

            owner=user,

            parent=None

        ).order_by("name")


    @staticmethod
    def get_children(user, folder_id):

        return Folder.objects.filter(

            owner=user,

            parent_id=folder_id

        ).order_by("name")


    @staticmethod
    def rename_folder(user, folder_id, name):

        folder = Folder.objects.get(

            id=folder_id,

            owner=user

        )

        folder.name = name

        folder.save()

        return folder


    @staticmethod
    def delete_folder(user, folder_id):

        folder = Folder.objects.get(

            id=folder_id,

            owner=user

        )

        folder.delete()