from django.db import models
from django.contrib.auth.models import User

class VaultEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")

    ciphertext = models.BinaryField()
    iv = models.BinaryField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

