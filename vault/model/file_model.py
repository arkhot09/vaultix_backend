from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="folders")
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="children")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:

        unique_together = ("owner","parent","name")

    def __str__(self):

        return self.name


class VaultFile(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vault_files"
    )

    folder = models.ForeignKey(
        Folder,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="files"
    )

    filename = models.CharField(
        max_length=255
    )

    original_name = models.CharField(
        max_length=255
    )

    extension = models.CharField(
        max_length=20
    )

    mime_type = models.CharField(
        max_length=255
    )

    file_size = models.BigIntegerField()

    encrypted_file = models.FileField(
        upload_to="encrypted_files/"
    )

    iv = models.CharField(
        max_length=255
    )

    encrypted_key = models.BinaryField(
        null=True,
    blank=True
    )
    algorithm = models.CharField(
        max_length=20,
        default="AES-GCM")
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.original_name