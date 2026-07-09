from .password_health_service import(PasswordHealthService)
from django.shortcuts import get_object_or_404

from ..model.vault_model import (
    VaultEntry
)


class VaultService:

    @staticmethod
    def create_entry(
        user,
        validated_data
    ):
        entry = VaultEntry.objects.create(
            user=user,
            title=validated_data["title"],
            ciphertext = validated_data["ciphertext"].encode("utf-8"), 
            iv = validated_data["iv"].encode("utf-8")
        )
        health = validated_data.get("health")

        if health:

            PasswordHealthService.create_health_record(
                user=user,
                title=validated_data["title"],
                health_data=health
            )
        return entry

    @staticmethod
    def get_entries(user):

        entries = VaultEntry.objects.filter(
            user=user
        )

        return [
            {
                "id": entry.id,
                "title": entry.title,
                "ciphertext":entry.ciphertext.decode("utf-8"),
                "iv":entry.iv.decode("utf-8"),
                "created_at":entry.created_at.isoformat(),
                "updated_at":entry.updated_at.isoformat()
            }
            for entry in entries
        ]

    @staticmethod
    def update_entry(
        user,
        entry_id,
        validated_data
    ):
        entry = get_object_or_404(
            VaultEntry,
            id=entry_id,
            user=user
        )

        entry.title = validated_data.get(
            "title",
            entry.title
        )

        entry.ciphertext = (
            validated_data["ciphertext"]
            .encode("utf-8")
        )

        entry.iv = (
            validated_data["iv"]
            .encode("utf-8")
        )

        entry.save()

        return entry

    @staticmethod
    def delete_entry(
        user,
        entry_id
    ):
        entry = get_object_or_404(
            VaultEntry,
            id=entry_id,
            user=user
        )

        entry.delete()