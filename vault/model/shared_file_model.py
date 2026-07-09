from django.db import models
from django.contrib.auth.models import User

from .file_model import VaultFile


class SharedVaultFile(models.Model):

    file = models.ForeignKey(
        VaultFile,
        on_delete=models.CASCADE,
        related_name="shared_entries"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shared_files_sent"
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shared_files_received"
    )

    encrypted_key = models.BinaryField()

    shared_at = models.DateTimeField(
        auto_now_add=True
    )

    revoked = models.BooleanField(
        default=False
    )

    class Meta:

        unique_together = (
            "file",
            "recipient"
        )

    def __str__(self):

        return f"{self.file.original_name} -> {self.recipient.username}"