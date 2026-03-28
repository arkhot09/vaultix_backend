from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class CryptoService:

    @staticmethod
    def encrypt(data: bytes, key: bytes):
        iv = os.urandom(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(iv, data, None)
        return iv, ciphertext

    @staticmethod
    def decrypt(iv: bytes, ciphertext: bytes, key: bytes):
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(iv, ciphertext, None)