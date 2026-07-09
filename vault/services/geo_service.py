from ..model.user_model import TrustedLocation
from ..services.location_service import LocationService


class GeoService:

    @staticmethod
    def is_suspicious_login(
        user,
        latitude=None,
        longitude=None
    ):

        if latitude is None or longitude is None:
            return False

        locations = TrustedLocation.objects.filter(
            user=user
        )

        if not locations.exists():
            return False

        for location in locations:

            distance = LocationService.distance_m(
                location.latitude,
                location.longitude,
                latitude,
                longitude
            )

            if distance <= location.radius:
                return False

        return True