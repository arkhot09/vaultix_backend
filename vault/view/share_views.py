from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.share_serializers import (ShareEntrySerializer)
from ..services.share_service import(ShareService)
from ..utils.responses import (success_response)
from ..model.share_model import (
    SharedEntry
)


class ShareEntry(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = (
            ShareEntrySerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        ShareService.share_entry(
            request.user,
            serializer.validated_data
        )

        return success_response(
            message="Entry shared."
        )

class SharedVaultView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        data = (
            ShareService
            .get_shared_entries(
                request.user
            )
        )

        return success_response(
            message="Shared entries retrieved.",
            data=data
        )

class RevokeShare(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,reqest,share_id):
        share = get_object_or_404(
            SharedEntry,
            id=share_id,
            sender=reqest.user
        )

        share.revoked=True

        share.save()

        return success_response(
            message="Access Revoked."
        )

class MySharedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = (
            ShareService
            .get_sent_shares(
                request.user
            )
        )

        return success_response(
            message="Shared Password retrived",
            data = data
        )
