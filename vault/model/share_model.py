from django.db import models
from django.contrib.auth.models import User
from .vault_model import VaultEntry
from django.utils import timezone

class SharedEntry(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')

    entry = models.ForeignKey(VaultEntry, on_delete=models.CASCADE)

    enc_sym_key = models.BinaryField()  
    ciphertext = models.BinaryField()   
    iv = models.BinaryField()           

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def is_accessiable(self):
        return not self.revoked and not self.is_expired()
    