from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)

from ..serializers.vault_serializers import (
    VaultEntrySerializer,
    UpdateVaultEntrySerializer
)

from ..services.vault_service import (
    VaultService
)

from ..utils.responses import (
    success_response
)

from ..model.user_model import (
    PasswordHealth
)

class CreateVaultEntry(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = (
            VaultEntrySerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        VaultService.create_entry(
            request.user,
            serializer.validated_data
        )

        return success_response(
            message="Vault entry stored."
        )

class GetVaultEntries(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        data = (
            VaultService.get_entries(
                request.user
            )
        )

        return success_response(
            message="Vault entries retrieved.",
            data=data
        )

class UpdateVaultEntry(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def put(
        self,
        request,
        entry_id
    ):

        serializer = (
            UpdateVaultEntrySerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        VaultService.update_entry(
            request.user,
            entry_id,
            serializer.validated_data
        )

        return success_response(
            message="Vault entry updated."
        )

class DeleteVaultEntry(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        entry_id
    ):

        VaultService.delete_entry(
            request.user,
            entry_id
        )

        return success_response(
            message="Vault entry deleted."
        )

class PasswordHealthView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        passwords = (
            PasswordHealth.objects.filter(
                user=request.user
            )
            .order_by("-created_at")
        )

        data = [
            {
                "title":
                    password.title,

                "strength":
                    password.strength,

                "score":
                    password.score,

                "is_reused":
                    password.is_reused,

                "is_common":
                    password.is_common,

                "created_at":
                    password.created_at.isoformat()
            }
            for password in passwords
        ]

        return success_response(
            message="Password health retrieved.",
            data=data
        )

