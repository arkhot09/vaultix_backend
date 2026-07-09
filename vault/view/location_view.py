from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..authentication.setup_token_authentication import (
    SetupTokenAuthentication
)
from ..services.location_service import LocationService
from ..serializers.location_serializers  import (TrustedLocationSerializer,CheckLocationSerializer)
from ..utils.responses import success_response

class TrustedLocationView(APIView):
    authentication_classes = [SetupTokenAuthentication]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        locations = LocationService.get_locations(
            request.user
        )

        data = [
            {
                "id": location.id,
                "name": location.name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "radius": location.radius,
                "created_at":location.created_at
            }

            for location in locations
        ]

        return success_response(
            message="Trusted locations retrieved.",
            data=data
        )

    def post(self, request):

        serializer = TrustedLocationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        LocationService.add_location(
            request.user,
            serializer.validated_data
        )

        return success_response(
            message="Trusted location added."
        )

class DeleteTrustedLocation(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        location_id
    ):

        LocationService.delete_location(
            request.user,
            location_id
        )

        return success_response(
            message="Trusted location removed."
        )


class CheckLocation(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = (
            CheckLocationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = (
            LocationService.check_location(
                request.user,
                serializer.validated_data
            )
        )

        return success_response(
            message="Location verified.",
            data=data
        )

