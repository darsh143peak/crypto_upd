import os
import json
import hashlib


class Handshake:

    def __init__(self):

        self.session_key = None


    # ---------- hello ----------

    def client_hello(self):

        print("Client: hello")


    def server_hello(self):

        print("Server: hello")


    # ---------- certificate ----------

    def send_certificate(self):

        print("Server: sending certificate")

        with open("cert/my_cert.json", "r") as f:
            cert = json.load(f)

        return cert


    def verify_certificate(self, cert):

        data = dict(cert)

        stored_hash = data.pop("hash")

        new_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        if stored_hash == new_hash:
            print("Client: certificate valid")
            return True

        print("Client: certificate invalid")
        return False


    # ---------- session key ----------

    def generate_session_key(self, save=True):

        key = os.urandom(16)

        self.session_key = key

        if save:
            with open("data/session.bin", "wb") as f:
                f.write(key)

        print("Session key created")

        return key


    def load_session_key(self):

        with open("data/session.bin", "rb") as f:
            key = f.read()

        self.session_key = key

        return key