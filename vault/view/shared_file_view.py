from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from ..serializers.shared_file_serializer import (ShareFileSerializer, SharedFileListSerializer)

from django.http import FileResponse
from ..services.shared_file_service import (

    SharedFileService

)

from ..utils.responses import success_response


class ShareFileView(APIView):

    permission_classes = [

        IsAuthenticated

    ]


    def post(

        self,

        request

    ):

        serializer = ShareFileSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        SharedFileService.share_file(

            request.user,

            serializer.validated_data

        )

        return success_response(

            message="File shared successfully."

        )

class SharedFilesView(APIView):
    

    permission_classes = [

        IsAuthenticated

    ]

    def get(self, request):

        files = SharedFileService.get_shared_files(

            request.user

        )

        serializer = SharedFileListSerializer(

            files,

            many=True

        )

        return success_response(

            message="Shared files.",

            data=serializer.data

        )
class SharedFileMetadataView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def get(

        self,

        request,

        share_id

    ):

        shared = SharedFileService.get_shared_metadata(

            request.user,

            share_id

        )

        return success_response(

            message="Metadata.",

            data={

                "file_id":
                    shared.id,

                "filename":
                    shared.file.original_name,

                "mime_type":
                    shared.file.mime_type,

                "iv":
                    shared.file.iv,

                "algorithm":
                    shared.file.algorithm,

                "encrypted_key":
                    shared.encrypted_key.decode()

            }

        )
    
class RevokeSharedFileView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def post(

        self,

        request,

        share_id

    ):

        SharedFileService.revoke(

            request.user,

            share_id

        )

        return success_response(

            message="Access revoked."

        )

class DownloadSharedFile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, share_id):

        file = SharedFileService.download_shared_file(
            request.user,
            share_id
        )

        return FileResponse(
            file.encrypted_file.open("rb"),
            as_attachment=True,
            filename=file.original_name
        )