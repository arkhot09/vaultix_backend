from .device_service import DeviceService
from .location_service import LocationService
from ..model.user_model import Profile

class SecurityService:
    @staticmethod
    def check_two_factor(profile):
        return profile.two_factor_enabled

    @staticmethod
    def check_device(user, request):
        return DeviceService.is_trusted_device(user,request)

    @staticmethod
    def check_location(user,request):

        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude is None or longitude is None:
            return False

        return LocationService.is_trusted_location (
            user,
            latitude,
            longitude
        )

    @staticmethod
    def check_security(user, request):
        profile = Profile.objects.get(
            user = user
        )

        status = {
            "2fa": SecurityService.check_two_factor(profile),
            "device": SecurityService.check_device(user,request),
            "location": SecurityService.check_location(user,request)
            }
        
        missing = [key
                   for key, value in status.items()
                   if not value
                   ]

        if not SecurityService.check_two_factor(profile):
            missing.append(SecurityRequirements.TWO_FACTOR)

        if not SecurityService.check_device(user, request):
            missing.append(SecurityRequirements.DEVICE)

        if not SecurityService.check_location(user, request):
            missing.append(SecurityRequirements.LOCATION)

        return{
            "security_complete":len(missing) == 0,
            "missing":missing,
            "status":status
        }

class SecurityRequirements:
        TWO_FACTOR = "2fa"
        DEVICE = "device"
        LOCATION = "location"


