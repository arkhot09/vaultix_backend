from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..model.file_model import VaultFile
from ..serializers.file_serializers import (FolderSerializer,UploadFileSerializer)
from ..services.file_service import (FileService)
from ..services.folder_service import (FolderService)
from ..utils.responses import (success_response)
from django.http import FileResponse
from ..model.file_model import Folder


class UploadFileView(APIView):
        
    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        serializer = UploadFileSerializer(

            data=request.data

        )

        serializer.is_valid(
            raise_exception=True
        )

        file = FileService.upload_file(

            request.user,

            serializer.validated_data

        )

        return success_response(

            message="File uploaded.",

            data={
                "id": file.id,
                "name": file.original_name
            }

        )

class FileListView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):

        parent_id = request.GET.get("folder")

        current_folder = None

        if parent_id:

            current_folder = Folder.objects.get(
                id=parent_id,
                owner=request.user
            )

            folders = FolderService.get_children(
                request.user,
                parent_id
            )

        else:

            folders = FolderService.get_root_folders(
                request.user
            )

        files = FileService.list_files(

            request.user,

            current_folder

        )

        folder_serializer = FolderSerializer(

            folders,

            many=True

        )

        data = []

        for file in files:

            data.append({

                "id": file.id,

                "filename": file.original_name,

                "size": file.file_size,

                "mime_type": file.mime_type,

                "folder": file.folder.id if file.folder else None,

                "created_at": file.created_at

            })

        return success_response(

            message="Contents retrieved.",

            data={

                "current_folder":
                    parent_id,

                "folders":
                    folder_serializer.data,

                "files":
                    data

            }

        )
    # def get(self, request):

        folder = request.GET.get("folder")

        files = VaultFile.objects.filter(
            owner=request.user
        )

        if folder:

            files = files.filter(
                folder_id=folder
            )

        else:

            files = files.filter(
                folder=None
            )

        files = files.order_by("-created_at")

        data = []

        for file in files:

            data.append({

                "id": file.id,

                "filename": file.original_name,

                "size": file.file_size,

                "mime_type": file.mime_type,

                "folder": file.folder.id if file.folder else None,

                "created_at": file.created_at

            })

        return success_response(

            message="Files retrieved",

            data=data

        )
class DownloadFileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        file_id
    ):

        file = VaultFile.objects.get(

            id=file_id,

            owner=request.user

        )

        return FileResponse(

            file.encrypted_file.open("rb"),

            as_attachment=True,

            filename=file.original_name + ".bin"

        )

class FileMetadataView(APIView):

    permission_classes = [IsAuthenticated]

    def get(

        self,

        request,

        file_id

    ):

        file = VaultFile.objects.get(

            id=file_id,

            owner=request.user

        )

        return success_response(

            message="Metadata",

            data={

                "encrypted_key":
                    file.encrypted_key.decode(),

                "iv":
                    file.iv,

                "algorithm":
                    file.algorithm,

                "filename":
                    file.original_name,

                "mime_type":
                    file.mime_type,
                "original_name":
                    file.original_name,

            }

        )