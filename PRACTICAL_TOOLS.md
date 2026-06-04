# Practical Crypto Tool Study

This project now includes a separate practical-study CLI:

```powershell
python .\tool_practical.py --help
```

The demos create files under `data/tool_practical/` so they do not disturb the main hide/extract workflow in `main.py`.

## Implemented Practical Demos

### 1. Tool Availability

```powershell
python .\tool_practical.py list
```

Shows whether OpenSSL, GnuPG, John the Ripper, Hashcat, Netcat, and Wireshark are installed on the system PATH.

### 2. OpenSSL

```powershell
python .\tool_practical.py openssl
```

Demonstrates:

- RSA private/public key generation.
- Self-signed certificate generation.
- Certificate verification.
- AES-256-CBC encryption and decryption from the command line.

If OpenSSL is not installed, the script prints the exact commands to run after installation.

### 3. GnuPG

```powershell
python .\tool_practical.py gnupg
```

Demonstrates:

- Public/private key creation.
- Message signing.
- Signature verification.
- Public-key encryption and private-key decryption.

The demo uses a local `GNUPGHOME` inside `data/tool_practical/gnupg/home`, so it does not mix with a user's personal GPG keyring.

### 4. Hashcat / John the Ripper

```powershell
python .\tool_practical.py password-attack
```

Demonstrates:

- Creating a weak SHA-256 password hash.
- Creating a small wordlist.
- Cracking the hash with a built-in Python dictionary attack.
- Printing John the Ripper and Hashcat commands for the same files.

The sample weak password is `crypto123`.

### 5. Netcat

```powershell
python .\tool_practical.py netcat
```

Demonstrates:

- Encrypting a message with the project's AES module.
- Preparing ciphertext for transfer over localhost.
- Printing Netcat sender and receiver commands.

Receiver terminal:

```powershell
nc -l -p 9999 > data/tool_practical/netcat/received_ciphertext.txt
```

Sender terminal:

```powershell
nc 127.0.0.1 9999 < data/tool_practical/netcat/ciphertext.txt
```

If Netcat is unavailable, use the Python fallback.

Receiver terminal:

```powershell
python .\tool_practical.py socket-receive
```

Sender terminal:

```powershell
python .\tool_practical.py socket-send
```

### 6. Wireshark

```powershell
python .\tool_practical.py wireshark
```

Demonstrates:

- Preparing encrypted localhost traffic.
- Capturing the traffic in Wireshark.
- Filtering with:

```text
tcp.port == 9999
```

Expected observation: the packet capture shows ciphertext, not the original plaintext.

## Run All Non-Interactive Demos

```powershell
python .\tool_practical.py all
```

This checks tool availability and runs the available practical demos. Missing external tools are reported with commands that can be tried after installation.

## Tools Kept as Separate Study

- CrypTool: useful for visual AES/RSA/hash/signature learning, but it does not need code integration here.
- ProVerif, AVISPA, Tamarin Prover, Scyther, CryptoVerif, EasyCrypt: useful for formal protocol verification, especially for modeling the toy handshake.
- Nikto: useful for web-server scanning, but this project is currently a local Python CLI, not a web application.
