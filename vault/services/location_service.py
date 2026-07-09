from math import (
    radians,
    sin,
    cos,
    sqrt,
    atan2
)

from ..model.user_model import (
    Profile,
    LoginLog
)

from ..model.user_model import (
    TrustedLocation
)


class LocationService:

    @staticmethod
    def distance_m(
        lat1,
        lon1,
        lat2,
        lon2
    ):

        R = 6371000

        dlat = radians(lat2 - lat1)

        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            +
            cos(radians(lat1))
            *
            cos(radians(lat2))
            *
            sin(dlon / 2) ** 2
        )

        c = (
            2
            *
            atan2(
                sqrt(a),
                sqrt(1 - a)
            )
        )

        return R * c

    @staticmethod
    def set_location(
        user,
        validated_data
    ):TrustedLocation.objects.create(
    user=user,
    name=validated_data["name"],
    latitude=validated_data["latitude"],
    longitude=validated_data["longitude"],
    radius=validated_data["radius"]
)

        
    @staticmethod
    def has_location(user):
        return TrustedLocation.objects.filter(
        user=user
    ).exists()

    @staticmethod
    def check_location(
        user,
        validated_data
    ):

        locations = TrustedLocation.objects.filter(
            user=user
        )

        if not locations.exists():

            return {
                "allowed": False,
                "distance": 0,
                "message": "No trusted locations configured."
            }

        current_lat = validated_data["latitude"]
        current_lng = validated_data["longitude"]

        nearest_location = None
        nearest_distance = float("inf")

        for location in locations:

            distance = LocationService.distance_m(
                location.latitude,
                location.longitude,
                current_lat,
                current_lng
            )

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_location = location

            if distance <= location.radius:

                LoginLog.objects.create(
                    user=user,
                    latitude=current_lat,
                    longitude=current_lng,
                    status="SUCCESS"
                )

                return {
                    "allowed": True,
                    "location": location.name,
                    "distance": round(distance)
                }

        LoginLog.objects.create(
            user=user,
            latitude=current_lat,
            longitude=current_lng,
            status="BLOCKED"
        )

        return {
            "allowed": False,
            "nearest_location":nearest_location.name,
            "distance": round(nearest_distance) ,
            "message": "Outside all trusted locations."
        }

    @staticmethod
    def add_location(
        user,
        validated_data
    ):

        return TrustedLocation.objects.create(
            user=user,
            name=validated_data["name"],
            latitude=validated_data["latitude"],
            longitude=validated_data["longitude"],
            radius=validated_data["radius"]
        )

    @staticmethod
    def get_locations(user):

        return TrustedLocation.objects.filter(
            user=user
        )

    @staticmethod
    def delete_location(
        user,
        location_id
    ):

        location = TrustedLocation.objects.get(
            id=location_id,
            user=user
        )

        location.delete()

    @staticmethod
    def is_trusted_location(
        user,
        latitude,
        longitude
    ):

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
                return True

        return False