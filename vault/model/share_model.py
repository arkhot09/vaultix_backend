from django.db import models
from django.contrib.auth.models import User
from .vault_model import VaultEntry

class SharedEntry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_owner')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)

    vault_entry = models.ForeignKey(VaultEntry, on_delete=models.CASCADE)

    ciphertext = models.BinaryField()

    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        if self.revoked:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True