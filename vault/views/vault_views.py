from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.crypto_services import CryptoService
from ..services.key_service import KeyService
from ..model.vault_model import VaultEntry
from ..model.user_model import Profile

class CreateVaultEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        VaultEntry.objects.create(
            user=request.user,
            title=request.data['title'],
            ciphertext=request.data['ciphertext'],
            iv=request.data['iv']
        )

        return Response({"message": "Stored securely"})
    
class GetVaultEntries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = VaultEntry.objects.filter(user=request.user)

        data = [
            {
                "id": e.id,
                "title": e.title,
                "ciphertext": e.ciphertext,
                "iv": e.iv
            }
            for e in entries
        ]

        return Response(data)
        
class UpdateVaultEntry(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, entry_id):
        entry = VaultEntry.objects.get(id=entry_id, user=request.user)

        password = request.data['password']
        new_data = request.data['data'].encode()

        profile = Profile.objects.get(user=request.user)
        key = KeyService.derive_key(password, profile.salt)

        iv, ciphertext = CryptoService.encrypt(new_data, key)

        entry.ciphertext = ciphertext
        entry.iv = iv
        entry.save()

        return Response({"message": "Updated"})
    
class DeleteVaultEntry(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, entry_id):
        entry = VaultEntry.objects.get(id=entry_id, user=request.user)
        entry.delete()

        return Response({"message": "Deleted"})
    
