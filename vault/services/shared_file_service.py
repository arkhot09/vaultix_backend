from django.contrib.auth.models import User

from ..model.file_model import VaultFile

from ..model.shared_file_model import SharedVaultFile


class SharedFileService:


    @staticmethod
    def share_file(

        sender,

        validated_data

    ):

        file = VaultFile.objects.get(

            id=validated_data["file_id"],

            owner=sender

        )

        recipient = User.objects.get(

            username=validated_data["recipient"]

        )

        share, created = SharedVaultFile.objects.update_or_create(

            file=file,

            recipient=recipient,

            defaults={

                "sender": sender,

                "encrypted_key":
                    validated_data[
                        "encrypted_key"
                    ].encode(),

                "revoked": False

            }

        )

        return share

    @staticmethod
    def get_shared_files(user):

        return SharedVaultFile.objects.filter(

            recipient=user,

            revoked=False

        ).select_related(

            "sender",

            "file"

        ).order_by(

            "-shared_at"

        )

    @staticmethod
    def get_shared_metadata(

        user,

        share_id

    ):

        return SharedVaultFile.objects.select_related(

            "file"

        ).get(

            id=share_id,

            recipient=user,

            revoked=False

        )

    @staticmethod
    def revoke(

        sender,

        share_id

    ):

        shared = SharedVaultFile.objects.get(

            id=share_id,

            sender=sender

        )

        shared.revoked = True

        shared.save()

        return shared


    @staticmethod
    def download_shared_file(user, share_id):
            
            shared = SharedVaultFile.objects.select_related(
                "file"
            ).get(
                id=share_id,
                recipient=user,
                revoked=False
            )

            return shared.file