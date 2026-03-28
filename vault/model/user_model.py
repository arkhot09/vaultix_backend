from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.BinaryField()
    public_key = models.BinaryField(null=True, blank=True)
    private_key_encrypted = models.BinaryField(null=True, blank=True)
    private_key_iv = models.BinaryField(null=True, blank=True)