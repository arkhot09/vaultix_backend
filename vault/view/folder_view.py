from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from vault.serializers.folder_serializer import FolderSerializer

from vault.services.folder_service import FolderService

from ..utils.responses import success_response
class FolderView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        folders = FolderService.get_root_folders(

            request.user

        )

        serializer = FolderSerializer(

            folders,

            many=True

        )
        return success_response(
    message="Folders retrieved",
    data=serializer.data
)


    def post(self, request):

        serializer = FolderSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        folder = FolderService.create_folder(

            request.user,

            serializer.validated_data

        )

        return success_response(

            message="Folder created",

            data=FolderSerializer(folder).data

        )
        
class FolderDetailView(APIView):


    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, folder_id):

        folder = FolderService.rename_folder(

            request.user,

            folder_id,

            request.data["name"]

        )

        return success_response(

            message="Folder renamed",

            data=FolderSerializer(folder).data

        )


    def delete(self, request, folder_id):

        FolderService.delete_folder(

            request.user,

            folder_id

        )

        return success_response(

            message="Folder deleted"

        )
        
class FolderChildrenView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request, folder_id):

        folders = FolderService.get_children(

            request.user,

            folder_id

        )

        serializer = FolderSerializer(

            folders,

            many=True

        )

        return success_response(

            message="Folder contents",

            data=serializer.data

        )