import secrets
from datetime import timedelta
from django.utils import timezone
from ..model.user_model import PendingLogin

class LoginTokenService:
    @staticmethod
    def create(user):
        PendingLogin.objects.filter(
            user=user
        ).delete()

        token = secrets.token_urlsafe(32)
        PendingLogin.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        return token

    @staticmethod
    def verify(token):
        try:
            pending = PendingLogin.objects.gets(
                token = token
            )

        except PendingLogin.DoesNotExist:
            return None

        if pending.expires_at < timezone.now():
            pending.delete()
            return None
        return pending.user

    @staticmethod
    def delete(token):
        PendingLogin.objects.filter(
            token = token
        ).delete()

        