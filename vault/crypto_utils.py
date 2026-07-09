import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.conf import settings


def decrypt_password(encrypted_b64: str) -> str:
    try:
        # ✅ Fix padding — Base64 strings must have length divisible by 4
        # + and = can get stripped/mangled in transit
        encrypted_b64 = encrypted_b64.strip()                    # remove whitespace
        padding_needed = len(encrypted_b64) % 4
        if padding_needed:
            encrypted_b64 += '=' * (4 - padding_needed)          # re-add stripped = padding

        raw        = base64.b64decode(encrypted_b64)
        iv         = raw[:16]
        ciphertext = raw[16:]

        print(f"[DEBUG] decoded length: {len(raw)}, iv: {iv.hex()}, ct length: {len(ciphertext)}")

        if len(iv) != 16:
            raise ValueError(f"IV must be 16 bytes, got {len(iv)}")
        if len(ciphertext) == 0:
            raise ValueError("Ciphertext is empty")

        key = hashlib.sha256(
            settings.TRANSPORT_ENCRYPTION_KEY.encode('utf-8')
        ).digest()

        cipher    = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')

    except (ValueError, KeyError) as e:
        raise ValueError(f"Password decryption failed: {e}")