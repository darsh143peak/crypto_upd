from myssl.handshake import Handshake

h = Handshake()

h.client_hello()

h.server_hello()

cert = h.send_certificate()

if h.verify_certificate(cert):

    h.generate_session_key()