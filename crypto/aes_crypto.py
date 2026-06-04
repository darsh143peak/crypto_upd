import base64
import hashlib
import os

try:
    from Crypto.Cipher import AES
except ImportError:
    AES = None

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    AESGCM = None


class AESCrypto:

    def __init__(self, key):

        if isinstance(key, str):
            key = key.encode()

        self.key = hashlib.sha256(key).digest()[:16]


    def encrypt(self, text):

        if AES is None:
            if AESGCM is None:
                raise RuntimeError("Install pycryptodome or cryptography to use AES encryption")

            nonce = os.urandom(12)
            ciphertext = AESGCM(self.key).encrypt(nonce, text.encode(), None)
            return base64.b64encode(nonce + ciphertext).decode()

        cipher = AES.new(self.key, AES.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(text.encode())

        data = cipher.nonce + tag + ciphertext

        return base64.b64encode(data).decode()


    def decrypt(self, enc):

        data = base64.b64decode(enc)

        if AES is None:
            if AESGCM is None:
                raise RuntimeError("Install pycryptodome or cryptography to use AES encryption")

            nonce = data[:12]
            ciphertext = data[12:]
            return AESGCM(self.key).decrypt(nonce, ciphertext, None).decode()

        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)

        text = cipher.decrypt_and_verify(ciphertext, tag)

        return text.decode()
