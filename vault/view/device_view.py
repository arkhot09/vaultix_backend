from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated)
from ..services.device_service import DeviceService
from ..utils.responses import success_response
from ..authentication.setup_token_authentication import (
    SetupTokenAuthentication
)

class TrustedDevicesView(APIView):
    authentication_classes = [SetupTokenAuthentication]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        devices = DeviceService.list_devices(
            request.user
        )

        data = [
            {
                "id": device.id,

                "device_name":
                    device.device_name,

                "browser":
                    device.browser,

                "operating_system":
                    device.operating_system,

                "ip_address":
                    device.ip_address,

                "is_trusted":
                    device.is_trusted,

                "first_login":
                    device.first_login,

                "last_used":
                    device.last_used
            }

            for device in devices
        ]

        return success_response(
            message="Trusted devices retrieved.",
            data=data
        )

class RegisterTrustedDevice(APIView):
    authentication_classes = [SetupTokenAuthentication]

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        DeviceService.register_device(
            request.user,
            request
        )

        return success_response(
            message="Device registered successfully."
        )

class DeleteTrustedDevice(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        device_id
    ):

        DeviceService.delete_device(
            request.user,
            device_id
        )

        return success_response(
            message="Trusted device removed."
        )