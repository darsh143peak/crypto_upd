import json
import hashlib


def verify_certificate(path):

    with open(path, "r") as f:
        cert = json.load(f)

    stored_hash = cert["hash"]

    data = dict(cert)
    data.pop("hash")

    new_hash = hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

    return stored_hash == new_hash