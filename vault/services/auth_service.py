from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from time import perf_counter
from django.db import transaction
from .setup_token_service import (SetupTokenService)
from rest_framework.exceptions import (AuthenticationFailed)
from rest_framework_simplejwt.tokens import (RefreshToken)

from ..model.user_model import Profile

from ..crypto_utils import decrypt_password
from .security_service import SecurityService
from .rsa_service import RSAService
from .device_service import DeviceService
from .login_service import LoginService

class AuthService:

    @staticmethod
    @transaction.atomic
    def register(validated_data):

        encrypted_password = validated_data.pop(
            "password"
        )


        try:
            password = decrypt_password(
                encrypted_password
            )

        except Exception:
            raise AuthenticationFailed(
                "Password decryption failed."
            )

        keys = RSAService.generate_key_pair()

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=password
        )
        setup_token = SetupTokenService.generate(user)

        Profile.objects.create(
            user=user,
            salt=validated_data["vault_salt"],
            vault_verifier=validated_data[
                "vault_verifier"
            ],
            public_key_pem=keys["public_key"],
            private_key_encrypted=b"",
            private_key_iv=b""
        )

        return {
            "private_key": keys["private_key"],
            "salt": validated_data["vault_salt"],
             "setup_token":setup_token
        }


    @staticmethod
    def generate_tokens(user):

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(
                refresh.access_token
            ),
            "refresh": str(refresh)
        }

    # @staticmethod
    # def login(
    #     request,
    #     validated_data
    # ):
    #     start = perf_counter()

    #     username = validated_data["username"]
    #     encrypted_password = validated_data["password"]

    #     latitude = validated_data.get("latitude")
    #     longitude = validated_data.get("longitude")

    #     # Decrypt password
    #     t = perf_counter()

    #     try:
    #         password = decrypt_password(
    #             encrypted_password
    #         )
    #     except Exception:
    #         raise AuthenticationFailed(
    #             "Password decryption failed."
    #         )

    #     print(
    #         f"Decrypt Password: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 2: Authenticate user
    #     # -------------------------------
    #     t = perf_counter()

    #     user = authenticate(
    #         username=username,
    #         password=password
    #     )

    #     print(
    #         f"Authenticate: {perf_counter() - t:.4f}s"
    #     )

    #     if not user:

    #         existing_user = User.objects.filter(
    #             username=username
    #         ).first()

    #         if existing_user:

    #             LoginService.create_log(
    #                 user=existing_user,
    #                 status="FAILED",
    #                 latitude=latitude,
    #                 longitude=longitude
    #             )

    #         raise AuthenticationFailed(
    #             "Invalid username or password."
    #         )

    #     # -------------------------------
    #     # Step 3: Load Profile
    #     # -------------------------------
    #     t = perf_counter()

    #     try:
    #         profile = Profile.objects.get(
    #             user=user
    #         )

    #     except Profile.DoesNotExist:
    #         raise AuthenticationFailed(
    #             "User profile not found."
    #         )

    #     print(
    #         f"Load Profile: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 4: Device Detection
    #     # -------------------------------
    #     t = perf_counter()

    #     device_info = (
    #         DeviceService.detect_new_device(
    #             user,
    #             request
    #         )
    #     )

    #     print(
    #         f"Device Detection: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 5: Geo Check
    #     # -------------------------------
    #     t = perf_counter()

    #     suspicious = (
    #         GeoService.is_suspicious_login(
    #             user,
    #             latitude,
    #             longitude
    #         )
    #     )

    #     print(
    #         f"Geo Check: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 6: Login Log
    #     # -------------------------------
    #     t = perf_counter()

    #     LoginService.create_log(
    #         user=user,
    #         status="SUCCESS",
    #         latitude=latitude,
    #         longitude=longitude,
    #         browser=device_info["browser"],
    #         operating_system=device_info[
    #             "operating_system"
    #         ],
    #         ip_address=device_info[
    #             "ip_address"
    #         ],
    #         is_suspicious=suspicious
    #     )

    #     print(
    #         f"Save Login Log: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 7: Security Score
    #     # -------------------------------
    #     t = perf_counter()

    #     LoginService.update_security_score(
    #         user
    #     )

    #     profile.refresh_from_db()

    #     print(
    #         f"Security Score: {perf_counter() - t:.4f}s"
    #     )

    #     # -------------------------------
    #     # Step 8: Generate JWT
    #     # -------------------------------
    #     t = perf_counter()

    #     tokens = AuthService.generate_tokens(
    #         user
    #     )

    #     print(
    #         f"JWT Generation: {perf_counter() - t:.4f}s"
    #     )

    #     print(
    #         f"TOTAL LOGIN TIME: {perf_counter() - start:.4f}s"
    #     )

    #     # -------------------------------
    #     # Response
    #     # -------------------------------
    #     return {

    #         "tokens": tokens,

    #         "user": {
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email
    #         },

    #         "security": {
    #             "security_score":
    #                 profile.security_score,

    #             "two_factor_enabled":
    #                 profile.two_factor_enabled,

    #             "suspicious_login":
    #                 suspicious
    #         },

    #         "device": {

    #             "new_device_detected":
    #                 device_info["is_new"],

    #             "device_name":
    #                 device_info["device_name"],

    #             "ip_address":
    #                 device_info["ip_address"]
    #         }
    #     }

    @staticmethod
    def login(
        request,
        validated_data
    ):
        

        username = validated_data["username"]

        encrypted_password = validated_data[
            "password"
        ]

        latitude = validated_data.get("latitude")

        longitude = validated_data.get("longitude")

        try:
            password = decrypt_password(
                encrypted_password
            )

        except Exception:
            raise AuthenticationFailed(
                "Password decryption failed."
            )
        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            existing_user = User.objects.filter(
                username=username
            ).first()

            if existing_user:

                LoginService.create_log(
                    user=existing_user,
                    status="FAILED",
                    latitude=latitude,
                    longitude=longitude
                )

            raise AuthenticationFailed(
                "Invalid username or password."
            )

        profile = Profile.objects.get(user=user)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise AuthenticationFailed(
                "User profile not found."
                )

        device_info = DeviceService.get_device_info(
            request
            )

        ip_address = DeviceService.get_client_ip(
            request
            )
        
        LoginService.create_log(
            user=user,
            status="SUCCESS",
            latitude=latitude,
            longitude=longitude,
            browser=device_info["browser"],
            operating_system=device_info["operating_system"],
            ip_address=ip_address,
            is_suspicious=False
        )

        LoginService.update_security_score(
            user
        )
        setup_token = SetupTokenService.generate(user)
        profile.refresh_from_db()
        security = SecurityService.check_security(
            user,request)
        if not security["security_complete"]:
            return {
                "message": "Security setup required.",
                "security_complete": False,
                "missing": security["missing"],
                "status": security["status"],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                    },
                 "setup_token":setup_token,
                    }
        tokens = AuthService.generate_tokens(user)

        return {
            "message":"Authentication Successful...",
            "security_complete": True,
            "tokens": tokens,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "security": {
                "security_score":profile.security_score,
                "two_factor_enabled":profile.two_factor_enabled
            }
        }