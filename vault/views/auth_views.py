from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..services.key_service import KeyService

class RegisterView(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.create_user(username=username, password=password)

        salt = KeyService.generate_salt()

        from ..model.user_model import Profile
        Profile.objects.create(user=user, salt=salt)

        return Response({"message": "User created"})