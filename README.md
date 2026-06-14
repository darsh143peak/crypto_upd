# Crypto Professor Demo

An educational cryptography project that combines a custom Python CLI, a React + Flask demo dashboard, and practical security-tool labs. It is designed to make core crypto ideas easy to demonstrate: handshake-style key setup, certificate checking, AES encryption, image steganography, OTP, pond authentication, GAN-assisted key material, and real-world tools such as OpenSSL, GnuPG, Hashcat, John the Ripper, Netcat, and Wireshark.

> This project is for learning and demonstration. It is not production-grade cryptography.

## Features

- Custom hide/extract workflow in `main.py`
- AES encryption with `pycryptodome` or `cryptography` fallback
- Image steganography using least-significant-bit pixel encoding
- JSON certificate creation and verification
- SSL-style handshake simulation
- GAN/noise-assisted key material generation
- OTP and pond-based access checks
- React dashboard for professor-friendly demos
- Flask API that reuses the existing Python modules
- Practical crypto-tool study CLI in `tool_practical.py`

## Project Structure

```text
auth/                 OTP and pond authentication
cert/                 Digital certificate creation and verification
crypto/               AES encryption/decryption
data/                 Images, session files, GAN noise, demo artifacts
emoji/                Base64-to-emoji encoder/decoder helpers
gan/                  Generator, discriminator, key noise, attacker scoring
myssl/                SSL-style handshake simulation
steg/                 Image steganography
src/                  React dashboard
tools/                Bundled external tools such as John and Hashcat
main.py               Original terminal hide/extract workflow
web_api.py            Flask backend for the React dashboard
tool_practical.py     Practical external-tool demo CLI
PRACTICAL_TOOLS.md    Detailed practical-tool guide
```

## Setup

Install Python dependencies:

```powershell
python -m pip install -r require.txt
```

Install React dependencies:

```powershell
npm.cmd install
```

Optional Python enhancements:

```powershell
python -m pip install pycryptodome torch
```

`pycryptodome` enables the AES EAX path. `torch` enables the GAN modules to use the PyTorch generator/discriminator instead of fallback randomness/scoring.

## Run The React Demo

Start the Flask backend:

```powershell
python web_api.py
```

In another terminal, start the React app:

```powershell
npm.cmd run dev
```

Open:

```text
http://127.0.0.1:5173
```

The dashboard includes:

- `Project Flow`: visual explanation of how modules connect
- `Hide Secret`: runs handshake, key generation, AES, steganography, OTP, pond auth, and certificate checks
- `Extract Secret`: recovers and decrypts the hidden message
- `Practical Tools`: runs or explains OpenSSL, GnuPG, password attack, Netcat, and Wireshark demos
- `Artifacts`: shows generated files and previews

## Run The Original CLI

```powershell
python main.py
```

Choose:

```text
hide
extract
```

The hide flow encrypts text and stores ciphertext inside `data/output.png`. The extract flow reads `data/output.png`, decrypts the embedded ciphertext, and prints the original secret.

## Practical Tool CLI

Show available tools:

```powershell
python tool_practical.py list
```

Run all non-interactive practical demos:

```powershell
python tool_practical.py all
```

Run individual demos:

```powershell
python tool_practical.py openssl
python tool_practical.py gnupg
python tool_practical.py password-attack
python tool_practical.py netcat
python tool_practical.py wireshark
```

See [PRACTICAL_TOOLS.md](PRACTICAL_TOOLS.md) for the full practical-tool guide.

## Important Generated Files

```text
data/input.png                       Original carrier image
data/output.png                      Stego image with hidden ciphertext
data/session.bin                     Session key from handshake flow
data/gan_noise.bin                   GAN/random noise mixed into final key
cert/my_cert.json                    Demo certificate
data/tool_practical/*                Practical-tool lab artifacts
```

## Demo Story For Professor

1. Open the React dashboard.
2. Start with `Project Flow` to explain the architecture.
3. Run `Hide Secret` to show the full encryption and hiding pipeline.
4. Show `Artifacts` and preview `data/output.png`.
5. Run `Extract Secret` to recover the message.
6. Open `Practical Tools` to connect the project to real tools:
   - OpenSSL for AES/RSA/certificates
   - GnuPG for signing and public-key encryption
   - Password Attack for attacker perspective
   - Netcat for encrypted transfer
   - Wireshark for packet inspection

## Notes

- Missing external tools should not break the demo. The practical CLI and dashboard print fallback commands where possible.
- `main.py` is kept as the terminal version of the project.
- `web_api.py` is the web-demo backend and avoids terminal `input()` calls.
- The password entered in `main.py` is currently collected for interaction but is not part of the key derivation flow.
