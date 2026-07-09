
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..model.user_model import Profile, LoginLog
from ..serializers.profile_serializer import ProfileSerializer
from ..services.security_score_service import calculate_security_score
from ..utils.responses import (
    success_response
)

class MyProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = Profile.objects.get(user=request.user)

        serializer = ProfileSerializer(profile)

        data = serializer.data

        return success_response(message="Profile Fetched Successfully!!!",
                                data=data)


class UpdateProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            # UPDATE SECURITY SCORE
            calculate_security_score(request.user)
            data = serializer.data
            return success_response(message= "Profile Updated Successfully!!!",
                data=data)

        return Response(serializer.errors, status=400)


class ProfileDashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = Profile.objects.get(user=request.user)

        # UPDATE SCORE EVERY TIME DASHBOARD LOADS
        calculate_security_score(request.user)

        profile.refresh_from_db()

        login_count = LoginLog.objects.filter(
            user=request.user
        ).count()

        successful_logins = LoginLog.objects.filter(
            user=request.user,
            status='SUCCESS'
        ).count()

        blocked_logins = LoginLog.objects.filter(
            user=request.user,
            status='BLOCKED'
        ).count()

        recent_logins = LoginLog.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

        recent_login_data = [
            {
                "latitude": log.latitude,
                "longitude": log.longitude,
                "status": log.status,
                "time": log.created_at
            }
            for log in recent_logins
        ]

        return Response({
            "security_score": profile.security_score,
            "weak_password_count": profile.weak_password_count,
            "reused_password_count": profile.reused_password_count,
            "login_count": login_count,
            "successful_logins": successful_logins,
            "blocked_logins": blocked_logins,
            "two_factor_enabled": profile.two_factor_enabled,
            "profile_completed": profile.profile_completed,
            "recent_logins": recent_login_data
        })

# class TrustedLocationView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         locations = (
#             LocationService.get_locations(
#                 request.user
#             )
#         )

#         data = [
#             {
#                 "id": loc.id,
#                 "name": loc.name,
#                 "latitude": loc.latitude,
#                 "longitude": loc.longitude,
#                 "radius": loc.radius
#             }
#             for loc in locations
#         ]

#         return success_response(
#             message="Locations retrieved.",
#             data=data
#         )

#     def post(self, request):

#         serializer = (
#             TrustedLocationSerializer(
#                 data=request.data
#             )
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         LocationService.add_location(
#             request.user,
#             serializer.validated_data
#         )

#         return success_response(
#             message="Location added."
#         )

