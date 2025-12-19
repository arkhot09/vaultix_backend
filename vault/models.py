from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.BinaryField()
    public_key_pem = models.TextField(blank=True, null=True)
    private_key_encrypted = models.BinaryField(blank=True, null=True)
    private_key_iv = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class VaultEntry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.CharField(max_length=191)
    login = models.CharField(max_length=191)
    ciphertext = models.BinaryField()
    iv = models.BinaryField()
    salt = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

class SharedEntry(models.Model):
    entry = models.ForeignKey(VaultEntry, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_shares')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shares')

    enc_sym_key = models.BinaryField()
    iv = models.BinaryField()
    ciphertext = models.BinaryField()

    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        if self.revoked:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

# class SharedEntry(models.Model):
#     entry = models.ForeignKey(VaultEntry, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_shares')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shares')
#     enc_sym_key = models.BinaryField()
#     iv = models.BinaryField()
#     ciphertext = models.BinaryField()
#     created_at = models.DateTimeField(auto_now_add=True)
