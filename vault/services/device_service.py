from user_agents import parse

from ..model.user_model import TrustedDevice


class DeviceService:

    @staticmethod
    def get_client_ip(request):

        forwarded = request.META.get(
            "HTTP_X_FORWARDED_FOR"
        )

        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def get_device_info(request):

        user_agent_string = request.META.get(
            "HTTP_USER_AGENT",
            ""
        )

        agent = parse(user_agent_string)

        browser = agent.browser.family

        operating_system = agent.os.family

        device_name = (
            f"{browser} on {operating_system}"
        )

        return {
            "browser": browser,
            "operating_system": operating_system,
            "device_name": device_name
        }

    @staticmethod
    def is_trusted_device(
        user,
        request
    ):

        info = DeviceService.get_device_info(
            request
        )

        ip = DeviceService.get_client_ip(
            request
        )

        return TrustedDevice.objects.filter(

            user=user,

            device_name=info["device_name"],

            ip_address=ip,

            is_trusted=True

        ).exists()

    @staticmethod
    def register_device(
        user,
        request
    ):

        info = DeviceService.get_device_info(
            request
        )

        ip = DeviceService.get_client_ip(
            request
        )

        device = TrustedDevice.objects.filter(
            user=user,
            device_name=info["device_name"],
            ip_address=ip
            ).first()
        if device:
            return device
        
        return TrustedDevice.objects.create(

            user=user,

            device_name=info["device_name"],

            browser=info["browser"],

            operating_system=info["operating_system"],

            ip_address=ip,

            is_trusted=True

        )

    @staticmethod
    def list_devices(user):

        return TrustedDevice.objects.filter(
            user=user
        )

    @staticmethod
    def delete_device(
        user,
        device_id
    ):

        device = TrustedDevice.objects.get(

            id=device_id,

            user=user

        )

        device.delete()