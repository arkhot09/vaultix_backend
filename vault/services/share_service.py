from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ..model.share_model import (
    SharedEntry
)

from ..model.vault_model import (
    VaultEntry
)


class ShareService:

    @staticmethod
    def share_entry(
        sender,
        validated_data
    ):

        recipient = get_object_or_404(
            User,
            username=validated_data[
                "recipient"
            ]
        )

        entry = get_object_or_404(
            VaultEntry,
            id=validated_data["entry_id"],
            user=sender
        )

        SharedEntry.objects.create(
            sender=sender,
            recipient=recipient,
            entry=entry,

            enc_sym_key=
                validated_data[
                    "enc_sym_key"
                ].encode(),

            ciphertext=
                validated_data[
                    "ciphertext"
                ].encode(),

            iv=
                validated_data[
                    "iv"
                ].encode(),

            expires_at=
                validated_data.get(
                    "expires_at"
                )
        )

    @staticmethod
    def get_shared_entries(user):

        entries = SharedEntry.objects.filter(
            recipient=user,
            revoked=False
        )

        return [
            {
                "id":
                    entry.id,

                "sender":
                    entry.sender.username,

                "enc_sym_key":
                    entry.enc_sym_key.decode(),

                "ciphertext":
                    entry.ciphertext.decode(),

                "iv":
                    entry.iv.decode(),

                "expires_at":
                    (
                        entry.expires_at.isoformat()
                        if entry.expires_at
                        else None
                    ),

                "expired":
                    entry.is_expired()
            }
            for entry in entries
            if entry.is_accessiable()
        ]

    
    @staticmethod
    def get_sent_shares(user):
        shares = SharedEntry.objects.filter(
            sender = user
        ).select_related(
            'recipient'
        )

        result = []

        for share in shares:

            if share.revoked:
                status = "REVOKED"

            elif share.is_expired():
                status = "EXPIRED"

            else:
                status = "ACTIVE"

            result.append({

                "id": share.id,
                "recipient": share.recipient.username,
                "created_at": share.created_at,
                "expires_at": share.expires_at,
                "status":status,
                "revoked":share.revoked
            })

        return result