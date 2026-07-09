from ..model.user_model import (
    PasswordHealth,
    Profile
)

from .security_score_service import (
    calculate_security_score
)


class PasswordHealthService:

    @staticmethod
    def create_health_record(
        user,
        title,
        health_data
    ):

        password_hash = (
            health_data["password_hash"]
        )

        reused = (
            PasswordHealth.objects.filter(
                user=user,
                password_hash=password_hash
            ).exists()
        )

        PasswordHealth.objects.create(
            user=user,
            title=title,

            password_hash=password_hash,

            strength=health_data[
                "strength"
            ],

            score=health_data[
                "score"
            ],

            is_common=health_data[
                "is_common"
            ],

            is_reused=reused
        )

        PasswordHealthService.update_profile(
            user
        )

    @staticmethod
    def update_profile(user):

        profile = Profile.objects.get(
            user=user
        )

        profile.weak_password_count = (
            PasswordHealth.objects.filter(
                user=user,
                strength="WEAK"
            ).count()
        )

        profile.reused_password_count = (
            PasswordHealth.objects.filter(
                user=user,
                is_reused=True
            ).count()
        )

        profile.save()

        calculate_security_score(
            user
        )