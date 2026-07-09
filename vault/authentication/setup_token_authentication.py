from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ..services.setup_token_service import (
    SetupTokenService
)


class SetupTokenAuthentication(
    BaseAuthentication
):

    def authenticate(
        self,
        request
    ):

        header = request.headers.get(
            "Authorization"
        )

        print("auth header:- ",header)

        if not header:

            return None

        if not header.startswith(
            "Bearer "
        ):

            return None

        token = header.split(" ")[1]

        user = SetupTokenService.verify(
            token
        )

        return (
            user,
            None
        )