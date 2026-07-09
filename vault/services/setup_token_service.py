from datetime import timedelta

from django.contrib.auth.models import User
from django.core import signing
from django.utils import timezone

from rest_framework.exceptions import AuthenticationFailed


class SetupTokenService:

    EXPIRY_MINUTES = 10

    @staticmethod
    def generate(user):

        payload = {
            "user_id": user.id,
            "expires_at": (
                timezone.now() +
                timedelta(
                    minutes=SetupTokenService.EXPIRY_MINUTES
                )
            ).timestamp()
        }

        return signing.dumps(
            payload,
            salt="vault-setup-token"
        )

    @staticmethod
    def verify(token):

        try:

            payload = signing.loads(
                token,
                salt="vault-setup-token"
            )

        except Exception:

            raise AuthenticationFailed(
                "Invalid setup token."
            )

        if timezone.now().timestamp() > payload["expires_at"]:

            raise AuthenticationFailed(
                "Setup token expired."
            )

        try:

            return User.objects.get(
                id=payload["user_id"]
            )

        except User.DoesNotExist:

            raise AuthenticationFailed(
                "User not found."
            )