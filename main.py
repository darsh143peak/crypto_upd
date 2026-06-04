import sys

from crypto.aes_crypto import AESCrypto
from emoji.encoder import EmojiEncoder
from emoji.decoder import EmojiDecoder
from steg.image_steg import ImageSteg
from auth.otp import OTP
from auth.pond_auth import PondAuth
from myssl.handshake import Handshake
from cert.verify import verify_certificate
from gan.gan_key import GANKey
from gan.attacker import Attacker
from gan.cipher_attack import CipherAttack

def exit_with(message):
    print(message)
    sys.exit(1)


def choose_pond():
    try:
        return int(input("Choose pond: "))
    except ValueError:
        exit_with("Invalid pond choice")


password = input("Enter password: ")

mode = input("Mode (hide / extract): ").strip().lower()

if mode not in ("hide", "extract"):
    exit_with("Invalid mode. Use 'hide' or 'extract'.")

h = Handshake()


# -------- session key --------

if mode == "hide":
    session_key = h.generate_session_key()
else:
    session_key = h.load_session_key()


# -------- handshake --------

h.client_hello()
h.server_hello()

cert = h.send_certificate()

if not h.verify_certificate(cert):
    exit_with("Handshake failed")


# -------- GAN key --------

gk = GANKey()
atk = Attacker()

cipher_atk = CipherAttack()
if mode == "hide":
    gan_noise = gk.generate_noise()
else:
    gan_noise = gk.load_noise()


final_key = session_key + gan_noise


# -------- attacker check (only for hide) --------

if mode == "hide":

    score = atk.try_key(final_key)

    print("Attacker score:", score)

    if score < 0.3:
        print("Weak key detected, regenerating")

        gan_noise = gk.generate_noise()

        final_key = session_key + gan_noise


# -------- crypto objects --------

aes = AESCrypto(final_key)

enc = EmojiEncoder()
dec = EmojiDecoder()
steg = ImageSteg()
otp = OTP()
pond = PondAuth(aes.key, 5)

# ---------------- HIDE ----------------

if mode == "hide":

    text = input("Enter secret text: ")

    # AES
    aes_text = aes.encrypt(text)
    steg.hide("data/input.png", "data/output.png", aes_text)

    print("Hidden in image.")
    score = cipher_atk.check_cipher(aes_text)

    print("Cipher attack score:", score)

    if score < 0.2:
        print("Cipher looks weak")
    # OTP
    code = otp.generate()
    print("OTP:", code)

    user = input("Enter OTP: ")

    if not otp.verify(user):
        exit_with("OTP FAILED")

    # Pond
    pond.generate()

    choice = choose_pond()

    if not pond.verify(choice):
        exit_with("Wrong pond")
    if not verify_certificate("cert/my_cert.json"):
        exit_with("Certificate invalid")

    print("Access allowed")


# ---------------- EXTRACT ----------------
elif mode == "extract":

    code = otp.generate()
    print("OTP:", code)

    user = input("Enter OTP: ")

    if not otp.verify(user):
        exit_with("OTP FAILED")

    pond.load()

    choice = choose_pond()

    if not pond.verify(choice):
        exit_with("Wrong pond")

    print("Access allowed")

    # -------- extract --------

    aes_text = steg.extract("data/output.png")

    text = aes.decrypt(aes_text)

    print("Secret:", text)


