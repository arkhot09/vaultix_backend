from ..model.user_model import LoginLog
from ..services.security_score_service import (
    calculate_security_score
)


class LoginService:

    @staticmethod
    def create_log(
        user,
        status,
        latitude=None,
        longitude=None,
        browser="",
        operating_system="",
        ip_address=None,
        is_suspicious=False
    ):

        return LoginLog.objects.create(
            user=user,
            latitude=latitude,
            longitude=longitude,
            status=status,
            browser=browser,
            operating_system=operating_system,
            ip_address=ip_address,
            is_suspicious=is_suspicious
        )

    @staticmethod
    def update_security_score(user):

        return calculate_security_score(user)