import pyotp
import qrcode
import base64

from io import BytesIO

from ..model.user_model import Profile

class TwoFactorService:

    @staticmethod
    def generate_secret(user):

        profile = Profile.objects.get(
            user=user
        )

        if not profile.two_factor_secret:
            profile.two_factor_secret = (
                pyotp.random_base32()
            )

            profile.save()

        return profile.two_factor_secret

    @staticmethod
    def generate_qr(user):
        profile = Profile.objects.get(user = user)

        secret = (
            TwoFactorService.generate_secret(
                user
            )
        )

        uri = pyotp.totp.TOTP(
            secret
        ).provisioning_uri(
            name=user.email,
            issuer_name="Vaultix"
        )

        qr = qrcode.make(uri)

        buffer = BytesIO()

        qr.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode()

    @staticmethod
    def verify(user, code):

        profile = Profile.objects.get(user = user)

        if not profile.two_factor_secret:
            return False

        totp = pyotp.TOTP(
            profile.two_factor_secret
        )

        return totp.verify(code)

    @staticmethod
    def enable(user):

        profile = Profile.objects.get(user = user)

        profile.two_factor_enabled = True

        profile.save()

    @staticmethod
    def disable(user):
        profile = Profile.objects.get(user = user)

        profile.two_factor_enabled = False

        profile.two_factor_secret = None

        profile.save()