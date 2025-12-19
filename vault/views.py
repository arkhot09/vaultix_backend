import os, json
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, VaultEntrySerializer
from .models import Profile, VaultEntry, SharedEntry

# crypto imports
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2


User = get_user_model()

def derive_key(password: str, salt: bytes, length=32):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt,
                     iterations=200000, backend=default_backend())
    return kdf.derive(password.encode())

# @ensure_csrf_cookie
# def csrf_token_view(request):
#     """
#     GET this endpoint from frontend to set a 'csrftoken' cookie that JS can read.
#     Browser will store the cookie and subsequent requests should include it via header.
#     """
#     return JsonResponse({'detail':'csrf cookie set'})

# @csrf_exempt
# def cookie_login(request):
#     """
#     POST {username, password} -> set HttpOnly access_token & refresh_token cookies
#     (csrf_exempt for login endpoint; consider other protections in production)
#     """
#     if request.method != 'POST':
#         return JsonResponse({'detail':'method not allowed'}, status=405)
#     import json
#     data = json.loads(request.body)
#     username = data.get('username'); password = data.get('password')
#     user = authenticate(username=username, password=password)
#     if not user:
#         return JsonResponse({'detail':'invalid'}, status=401)

#     refresh = RefreshToken.for_user(user)
#     access = str(refresh.access_token)
#     resp = JsonResponse({'detail':'login ok'})
#     # Set cookies
#     resp.set_cookie('access_token', access, httponly=True, secure=False, samesite='Lax')  # set secure=True in prod (HTTPS)
#     resp.set_cookie('refresh_token', str(refresh), httponly=True, secure=False, samesite='Lax')
#     return resp

# @csrf_exempt
# def cookie_logout(request):
#     resp = JsonResponse({'detail':'logged out'})
#     resp.delete_cookie('access_token')
#     resp.delete_cookie('refresh_token')
#     return resp


# Register 
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate RSA key pair
        rsa_key = RSA.generate(2048)
        private_key = rsa_key.export_key()
        public_key = rsa_key.publickey().export_key()

        # Derive encryption key from password
        password = request.data.get("password")
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32, count=200_000)

        # Encrypt private key
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_len = 16 - len(private_key) % 16
        padded = private_key + bytes([pad_len] * pad_len)
        encrypted_private = cipher.encrypt(padded)

        # Get or create profile (🔥 FIX)
        profile, created = Profile.objects.get_or_create(user=user)

        profile.salt = salt
        profile.public_key_pem = public_key.decode()
        profile.private_key_encrypted = encrypted_private
        profile.private_key_iv = iv
        profile.save()

        return Response({"message": "User registered securely"}, status=201)

    return Response(serializer.errors, status=400)
# def register_view(request):
#     """Register a new user and return success message"""
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response(
#             {"message": "User registered successfully", "id": user.id},
#             status=status.HTTP_201_CREATED
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login 

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
    """Login user and return JWT tokens in JSON"""
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username
    })


@api_view(["POST"])
def logout_view(request):
    """Logout user (client should clear stored tokens)"""
    return Response({"message": "Logged out"})

# WhoAmI
# Simple endpoint to check who the current user is (frontend can call to confirm login)

class WhoAmI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"username": request.user.username})




# Vault endpoints (protected via CookieJWTAuthentication)
class VaultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles both:
        1. Storing a new password (if site, login, password present)
        2. Fetching all passwords (if only master_password present)
        """

        master_password = request.data.get('master_password')

        # Fetch passwords
        if master_password and not request.data.get('site'):
            entries = VaultEntry.objects.filter(owner=request.user)
            data = []

            for e in entries:
                try:
                    # Derive AES key
                    key = PBKDF2(master_password, e.salt, dkLen=32, count=100_000)
                    cipher = AES.new(key, AES.MODE_CBC, e.iv)
                    decrypted = cipher.decrypt(e.ciphertext)
                    pad_len = decrypted[-1]
                    password_plaintext = decrypted[:-pad_len].decode()
                except Exception:
                    password_plaintext = None  # decryption failed

                data.append({
                    'id': e.id,
                    'site': e.site,
                    'login': e.login,
                    'password_plaintext': password_plaintext,
                    'created_at': e.created_at
                })

            return Response(data)

        # Store a new password
        site = request.data.get('site')
        login = request.data.get('login')
        password_plaintext = request.data.get('password')

        if not all([site, login, password_plaintext, master_password]):
            return Response({"error": "All fields are required."}, status=400)

        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        key = PBKDF2(master_password, salt, dkLen=32, count=100_000)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_len = AES.block_size - len(password_plaintext.encode()) % AES.block_size
        padded_password = password_plaintext.encode() + bytes([pad_len] * pad_len)
        ciphertext = cipher.encrypt(padded_password)

        entry = VaultEntry.objects.create(
            owner=request.user,
            site=site,
            login=login,
            ciphertext=ciphertext,
            iv=iv,
            salt=salt
        )

        return Response({"message": "Password saved successfully.", "id": entry.id})
    
#updated shareview
class ShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entry_id = request.data.get('entry_id')
        recipient_username = request.data.get('recipient')
        master_password = request.data.get('master_password')
        expiry_minutes = request.data.get('expiry_minutes')  # optional

        if not all([entry_id, recipient_username, master_password]):
            return Response({'detail': 'missing fields'}, status=400)

        entry = VaultEntry.objects.get(id=entry_id, owner=request.user)
        recipient = User.objects.get(username=recipient_username)
        recipient_profile = Profile.objects.get(user=recipient)
        sender_profile = Profile.objects.get(user=request.user)

        # 🔓 Decrypt sender password
        key_sender = PBKDF2(master_password, sender_profile.salt, dkLen=32, count=200_000)
        aes_sender = AES.new(key_sender, AES.MODE_CBC, entry.iv)
        decrypted = aes_sender.decrypt(entry.ciphertext)
        pad_len = decrypted[-1]
        plaintext = decrypted[:-pad_len]

        # 🔐 Hybrid encryption
        sym_key = os.urandom(32)
        aesgcm = AESGCM(sym_key)
        iv = os.urandom(12)
        ct = aesgcm.encrypt(iv, plaintext, None)

        rsa_pub = RSA.import_key(recipient_profile.public_key_pem.encode())
        enc_sym = PKCS1_OAEP.new(rsa_pub).encrypt(sym_key)

        expires_at = None
        if expiry_minutes:
            expires_at = timezone.now() + timedelta(minutes=int(expiry_minutes))

        SharedEntry.objects.create(
            entry=entry,
            sender=request.user,
            recipient=recipient,
            enc_sym_key=enc_sym,
            iv=iv,
            ciphertext=ct,
            expires_at=expires_at
        )

        return Response({'message': 'Password shared successfully'})

#recipient view feature for recipint

class SharedVaultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shared_id = request.data.get('shared_id')
        master_password = request.data.get('master_password')

        shared = SharedEntry.objects.get(
            id=shared_id,
            recipient=request.user
        )

        if not shared.is_valid():
            return Response({'detail': 'access expired or revoked'}, status=403)

        profile = Profile.objects.get(user=request.user)

        # 🔓 Decrypt private key
        key = PBKDF2(master_password, profile.salt, dkLen=32, count=200_000)
        cipher = AES.new(key, AES.MODE_CBC, profile.private_key_iv)
        decrypted = cipher.decrypt(profile.private_key_encrypted)
        pad_len = decrypted[-1]
        private_key = decrypted[:-pad_len]

        rsa_priv = RSA.import_key(private_key)

        sym_key = PKCS1_OAEP.new(rsa_priv).decrypt(shared.enc_sym_key)
        aesgcm = AESGCM(sym_key)
        plaintext = aesgcm.decrypt(shared.iv, shared.ciphertext, None)

        return Response({
            'site': shared.entry.site,
            'login': shared.entry.login,
            'password': plaintext.decode()
        })
    
#revoke view featurre for sender
class RevokeShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shared_id = request.data.get('shared_id')

        shared = SharedEntry.objects.get(
            id=shared_id,
            sender=request.user
        )

        shared.revoked = True
        shared.save()

        return Response({'message': 'Access revoked'})


# Sharing endpoints

# class ShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entry_id = request.data.get('entry_id')
        recipient_username = request.data.get('recipient')
        master_password = request.data.get('master_password')

        if not all([entry_id, recipient_username, master_password]):
            return Response({'detail': 'missing'}, status=400)

        try:
            entry = VaultEntry.objects.get(id=entry_id, owner=request.user)
        except VaultEntry.DoesNotExist:
            return Response({'detail': 'entry not found'}, status=404)

        try:
            recipient = User.objects.get(username=recipient_username)
            recipient_profile = Profile.objects.get(user=recipient)
        except User.DoesNotExist:
            return Response({'detail': 'recipient not found'}, status=404)

        sender_profile = Profile.objects.get(user=request.user)
        key_sender = derive_key(master_password, sender_profile.salt)
        aesgcm_sender = AESGCM(key_sender)
        try:
            plaintext = aesgcm_sender.decrypt(entry.iv, entry.ciphertext, None)
        except Exception:
            return Response({'detail': 'decrypt failed'}, status=400)

        # Hybrid encryption
        sym_key = os.urandom(32)
        aesgcm = AESGCM(sym_key)
        iv = os.urandom(12)
        ct = aesgcm.encrypt(iv, plaintext, None)

        rsa_pub = RSA.import_key(recipient_profile.public_key_pem.encode())
        rsa_cipher = PKCS1_OAEP.new(rsa_pub)
        enc_sym = rsa_cipher.encrypt(sym_key)

        shared = SharedEntry.objects.create(
            entry=entry, sender=request.user, recipient=recipient,
            enc_sym_key=enc_sym, iv=iv, ciphertext=ct
        )
        return Response({'detail': 'shared', 'shared_id': shared.id})