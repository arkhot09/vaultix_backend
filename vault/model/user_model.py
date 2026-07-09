from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vault_verifier = models.CharField(max_length=255,null=True,blank=True)
    # BASIC PROFILE
    full_name = models.CharField(max_length=150, blank=True)
    profile_image = models.ImageField(upload_to='profiles/',null=True,blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15,blank=True)
    location = models.CharField(max_length=255,blank=True)
    website = models.URLField(blank=True)
    profile_completed = models.BooleanField(default=False)
    # SECURITY
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=64,blank=True)
    # SECURITY ANALYTICS
    security_score = models.IntegerField(default=0)
    weak_password_count = models.IntegerField(default=0)
    reused_password_count = models.IntegerField(default=0)
    # CRYPTO
    salt = models.CharField(max_length=255)
    public_key_pem = models.TextField(null=True, blank=True)
    private_key_encrypted = models.BinaryField(null=True,blank=True)
    private_key_iv = models.BinaryField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class LoginLog(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('BLOCKED', 'Blocked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    browser = models.CharField( max_length=255, blank=True )
    operating_system = models.CharField( max_length=255, blank=True )
    ip_address = models.GenericIPAddressField( null=True, blank=True )
    is_suspicious = models.BooleanField( default=False )

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.created_at}"
    

class PasswordHealth(models.Model):

    STRENGTH_CHOICES = [
        ('WEAK', 'Weak'),
        ('MEDIUM', 'Medium'),
        ('STRONG', 'Strong'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    strength = models.CharField(max_length=10,choices=STRENGTH_CHOICES)
    score = models.IntegerField(default=0)
    is_reused = models.BooleanField(default=False)
    is_common = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class TrustedDevice(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    device_name = models.CharField(max_length=255)
    browser = models.CharField(max_length=255,blank=True)
    operating_system = models.CharField(max_length=255,blank=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    is_trusted = models.BooleanField(default=True)
    first_login = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.device_name}"

class TrustedLocation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trusted_locations"
    )

    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username}"
            f" - {self.name}"
        )


class PendingLogin(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.user.username