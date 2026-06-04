import json
import hashlib
from datetime import datetime


class DigitalCertificate:

    def __init__(self, name, email, public_key, issuer):

        self.name = name
        self.email = email
        self.public_key = public_key
        self.issuer = issuer
        self.date = str(datetime.now())


    def to_dict(self):

        return {
            "name": self.name,
            "email": self.email,
            "public_key": self.public_key,
            "issuer": self.issuer,
            "date": self.date
        }


    def generate_hash(self):

        data = json.dumps(self.to_dict(), sort_keys=True)

        return hashlib.sha256(data.encode()).hexdigest()


    def save(self, path):

        data = self.to_dict()

        data["hash"] = self.generate_hash()

        with open(path, "w") as f:
            json.dump(data, f, indent=4)
