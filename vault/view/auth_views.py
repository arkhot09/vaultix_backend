from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from ..authentication.setup_token_authentication import (
    SetupTokenAuthentication
)
from ..authentication.setup_token_authentication import (
    SetupTokenAuthentication
)
# from ...vault.model.user_model import (
from ..model.user_model import (
    Profile,
    LoginLog,
)

from ..serializers.auth_serializers import (
    RegisterSerializer,
    LoginSerializer,
    StorePrivateKeySerializer,
    VerifyTwoFactorSerializer
)

from ..services.auth_service import (
    AuthService
)

from ..utils.responses import (
    success_response,
    error_response
)

from ..services.two_factor_service import TwoFactorService

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = AuthService.register(
            serializer.validated_data
        )

        return success_response(
            message="User registered successfully.",
            data=data,
            status_code=201
        )

class LoginView(APIView):

        permission_classes = [AllowAny]

        def post(self, request):

            serializer = LoginSerializer(
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            data = AuthService.login(
                request=request,
                validated_data=serializer.validated_data
            )

            return success_response(
                message=data.pop("message"),
                data=data
            )

class StorePrivateKey(APIView):
        authentication_classes = [SetupTokenAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request):

            serializer = (
                StorePrivateKeySerializer(
                    data=request.data
                )
            )

            serializer.is_valid(
                raise_exception=True
            )

            profile = Profile.objects.get(
                user=request.user
            )

            profile.private_key_encrypted = (
                serializer.validated_data[
                    "ciphertext"
                ].encode()
            )

            profile.private_key_iv = (
                serializer.validated_data[
                    "iv"
                ].encode()
            )

            profile.save()

            return success_response(
                message="Private key stored."
            )

class GetPrivateKey(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):

            profile = Profile.objects.get(
                user=request.user
            )

            return success_response(
                message="Private key retrieved.",
                data={
                    "ciphertext":
                        profile.private_key_encrypted.decode(),

                    "iv":
                        profile.private_key_iv.decode()
                }
            )

class GetSalt(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):

            profile = Profile.objects.get(
                user=request.user
            )

            return success_response(
                message="Salt retrieved.",
                data={
                    "username":
                        request.user.username,

                    "salt":
                        profile.salt,

                    "vault_verifier":
                        profile.vault_verifier
                }
            )

class GetPublicKey(APIView):

        permission_classes = [IsAuthenticated]

        def get(
            self,
            request,
            username
        ):

            try:
                user = User.objects.get(
                    username=username
                )

                profile = Profile.objects.get(
                    user=user
                )

            except (
                User.DoesNotExist,
                Profile.DoesNotExist
            ):
                return error_response(
                    message="User not found.",
                    status_code=404
                )

            return success_response(
                message="Public key retrieved.",
                data={
                    "public_key_pem":
                        profile.public_key_pem
                }
            )

class LoginLogView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            logs = LoginLog.objects.filter(
                user=request.user
            ).order_by(
                "-created_at"
            )

            data = [
                {
                    "latitude":
                        log.latitude,

                    "longitude":
                        log.longitude,

                    "status":
                        log.status,

                    "time":
                        log.created_at.isoformat(),

                    "browser":
                        log.browser,

                    "operating_system":
                        log.operating_system,

                    "ip_address":
                        log.ip_address,

                    "is_suspicious":
                        log.is_suspicious
                }
                for log in logs
            ]

            return success_response(
                message="Login logs retrieved.",
                data=data
            )

# class TrustedDevicesView(APIView):

#         permission_classes = [IsAuthenticated]

#         def get(self, request):

#             devices = TrustedDevice.objects.filter(
#                 user=request.user
#             ).order_by(
#                 "-last_used"
#             )

#             data = [
#                 {
#                     "id":
#                         d.id,

#                     "device_name":
#                         d.device_name,

#                     "browser":
#                         d.browser,

#                     "operating_system":
#                         d.operating_system,

#                     "ip_address":
#                         d.ip_address,

#                     "is_trusted":
#                         d.is_trusted,

#                     "first_login":
#                         d.first_login.isoformat(),

#                     "last_used":
#                         d.last_used.isoformat()
#                 }
#                 for d in devices
#             ]

#             return success_response(
#                 message="Trusted devices retrieved.",
#                 data=data
#             )


class TwoFactorSetup(APIView):
      authentication_classes = [SetupTokenAuthentication]
      permission_classes = [IsAuthenticated]

      def get(self,request):
    
        qr = TwoFactorService.generate_qr(
                request.user
        )

        return success_response(
                message = "QR Generated",
                data= {
                    "qr":qr,
                    "secret":TwoFactorService.generate_secret(
                        request.user
                    )
                }
        )

class EnableTwoFactor(APIView):
    authentication_classes = [SetupTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

            serializer = VerifyTwoFactorSerializer(
                  data = request.data
            )

            serializer.is_valid(raise_exception=True)

            valid = TwoFactorService.verify(
                  request.user,
                  serializer.validated_data["code"]
            )

            if not valid:
                  return error_response(
                        message="Invalid OTP"
                  )
            TwoFactorService.enable(request.user)
            return success_response(
                  message="Two Factor Enabled"
            )


class DisableTwoFactor(APIView):
      permission_classes = [IsAuthenticated]

      def post(self, request):
            serializer = VerifyTwoFactorSerializer(
                  data = request.data
            )

            serializer.is_valid(
                  raise_exception=True
            )

            valid = TwoFactorService.verify(
                  request.user,
                  serializer.validated_data["code"]
            )

            if not valid:
                  return error_response(
                        message="Invalid OTP"
                  )

            TwoFactorService.disable(
                  request.user
            )

            return success_response(
                  message="Two Factor Disabled"
            )