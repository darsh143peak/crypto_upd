import argparse
import hashlib
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

from crypto.aes_crypto import AESCrypto


BASE_DIR = Path("data") / "tool_practical"
TOOLS_DIR = Path("tools")
MESSAGE = "This is a crypto practical message."
PASSWORD = "student123"
WEAK_PASSWORD = "crypto123"


KNOWN_TOOL_PATHS = {
    "openssl": [
        Path("C:/Program Files/OpenSSL-Win64/bin/openssl.exe"),
        Path("C:/Program Files/Git/mingw64/bin/openssl.exe"),
        Path("C:/Program Files/Git/usr/bin/openssl.exe"),
    ],
    "gpg": [
        Path("C:/Program Files/GnuPG/bin/gpg.exe"),
    ],
    "john": [
        TOOLS_DIR / "john-1.9.0-jumbo-1-win64" / "run" / "john.exe",
    ],
    "hashcat": [
        TOOLS_DIR / "hashcat-7.1.2" / "hashcat.exe",
    ],
    "ncat": [
        Path("C:/Program Files (x86)/Nmap/ncat.exe"),
        Path("C:/Program Files/Nmap/ncat.exe"),
    ],
    "wireshark": [
        Path("C:/Program Files/Wireshark/Wireshark.exe"),
    ],
    "tshark": [
        Path("C:/Program Files/Wireshark/tshark.exe"),
    ],
}


def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)


def tool_path(*names):
    for name in names:
        found = shutil.which(name)
        if found:
            return found
        for candidate in KNOWN_TOOL_PATHS.get(name.lower(), []):
            if candidate.exists():
                return str(candidate)
    return None


def run_command(command, cwd=None, env=None, input_text=None):
    print("\n$ " + " ".join(command))
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        input=input_text,
        text=True,
        capture_output=True,
    )

    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError("Command failed with exit code " + str(result.returncode))

    return result


def write_text(path, text):
    path.write_text(text, encoding="utf-8")
    print("Created:", path)


def print_missing_tool(tool, commands):
    print("\n" + tool + " was not found on PATH.")
    print("Install it, then run these commands manually from the project root:")
    for command in commands:
        print("  " + command)


def shell_quote(value):
    value = str(value)
    if " " in value:
        return '"' + value + '"'
    return value


def demo_openssl():
    demo_dir = BASE_DIR / "openssl"
    ensure_dir(demo_dir)

    message_path = demo_dir / "message.txt"
    encrypted_path = demo_dir / "message.enc"
    decrypted_path = demo_dir / "message.dec.txt"
    private_key = demo_dir / "private.pem"
    public_key = demo_dir / "public.pem"
    cert_path = demo_dir / "student-cert.pem"

    write_text(message_path, MESSAGE)

    openssl = tool_path("openssl")
    if not openssl:
        print_missing_tool(
            "OpenSSL",
            [
                "openssl genrsa -out data/tool_practical/openssl/private.pem 2048",
                "openssl rsa -in data/tool_practical/openssl/private.pem -pubout -out data/tool_practical/openssl/public.pem",
                "openssl req -new -x509 -key data/tool_practical/openssl/private.pem -out data/tool_practical/openssl/student-cert.pem -days 365 -subj \"/CN=Student Crypto Practical\"",
                "openssl verify -CAfile data/tool_practical/openssl/student-cert.pem data/tool_practical/openssl/student-cert.pem",
                "openssl enc -aes-256-cbc -pbkdf2 -salt -in data/tool_practical/openssl/message.txt -out data/tool_practical/openssl/message.enc -pass pass:student123",
                "openssl enc -d -aes-256-cbc -pbkdf2 -in data/tool_practical/openssl/message.enc -out data/tool_practical/openssl/message.dec.txt -pass pass:student123",
            ],
        )
        return

    run_command([openssl, "genrsa", "-out", str(private_key), "2048"])
    run_command([openssl, "rsa", "-in", str(private_key), "-pubout", "-out", str(public_key)])
    run_command(
        [
            openssl,
            "req",
            "-new",
            "-x509",
            "-key",
            str(private_key),
            "-out",
            str(cert_path),
            "-days",
            "365",
            "-subj",
            "/CN=Student Crypto Practical",
        ]
    )
    run_command([openssl, "verify", "-CAfile", str(cert_path), str(cert_path)])
    run_command(
        [
            openssl,
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-salt",
            "-in",
            str(message_path),
            "-out",
            str(encrypted_path),
            "-pass",
            "pass:" + PASSWORD,
        ]
    )
    run_command(
        [
            openssl,
            "enc",
            "-d",
            "-aes-256-cbc",
            "-pbkdf2",
            "-in",
            str(encrypted_path),
            "-out",
            str(decrypted_path),
            "-pass",
            "pass:" + PASSWORD,
        ]
    )
    print("\nOpenSSL practical complete.")
    print("Certificate:", cert_path)
    print("Encrypted file:", encrypted_path)
    print("Decrypted text:", decrypted_path.read_text(encoding="utf-8"))


def demo_gnupg():
    demo_dir = BASE_DIR / "gnupg"
    gnupg_home = demo_dir / "home"
    ensure_dir(gnupg_home)

    message_path = demo_dir / "message.txt"
    signed_path = demo_dir / "message.txt.asc"
    encrypted_path = demo_dir / "message.txt.gpg"
    decrypted_path = demo_dir / "message.dec.txt"
    write_text(message_path, MESSAGE)

    gpg = tool_path("gpg", "gpg2")
    if not gpg:
        print_missing_tool(
            "GnuPG",
            [
                "gpg --quick-generate-key \"Student Crypto <student@example.com>\" default default 1y",
                "gpg --armor --detach-sign data/tool_practical/gnupg/message.txt",
                "gpg --verify data/tool_practical/gnupg/message.txt.asc data/tool_practical/gnupg/message.txt",
                "gpg --encrypt --recipient \"Student Crypto <student@example.com>\" data/tool_practical/gnupg/message.txt",
                "gpg --decrypt data/tool_practical/gnupg/message.txt.gpg",
            ],
        )
        return

    env = os.environ.copy()
    env["GNUPGHOME"] = str(gnupg_home.resolve())
    key_id = "Student Crypto <student@example.com>"

    key_check = subprocess.run(
        [gpg, "--batch", "--list-secret-keys", key_id],
        env=env,
        text=True,
        capture_output=True,
    )
    if key_check.returncode != 0:
        run_command(
            [
                gpg,
                "--batch",
                "--pinentry-mode",
                "loopback",
                "--passphrase",
                "",
                "--quick-generate-key",
                key_id,
                "default",
                "default",
                "1y",
            ],
            env=env,
        )
    else:
        print("Using existing GnuPG demo key:", key_id)
    run_command([gpg, "--armor", "--yes", "--detach-sign", str(message_path)], env=env)
    run_command([gpg, "--verify", str(signed_path), str(message_path)], env=env)
    run_command(
        [
            gpg,
            "--yes",
            "--trust-model",
            "always",
            "--output",
            str(encrypted_path),
            "--encrypt",
            "--recipient",
            key_id,
            str(message_path),
        ],
        env=env,
    )
    run_command(
        [
            gpg,
            "--batch",
            "--yes",
            "--pinentry-mode",
            "loopback",
            "--passphrase",
            "",
            "--output",
            str(decrypted_path),
            "--decrypt",
            str(encrypted_path),
        ],
        env=env,
    )
    print("\nGnuPG practical complete.")
    print("Signature:", signed_path)
    print("Encrypted file:", encrypted_path)
    print("Decrypted text:", decrypted_path.read_text(encoding="utf-8"))


def demo_password_attack():
    demo_dir = BASE_DIR / "password_attack"
    ensure_dir(demo_dir)

    hash_path = demo_dir / "sha256_hash.txt"
    wordlist_path = demo_dir / "wordlist.txt"
    cracked_path = demo_dir / "python_cracked.txt"
    digest = hashlib.sha256(WEAK_PASSWORD.encode()).hexdigest()

    write_text(hash_path, digest + "\n")
    write_text(
        wordlist_path,
        "\n".join(["password", "student", "admin123", "crypto123", "letmein"]) + "\n",
    )

    cracked = None
    for candidate in wordlist_path.read_text(encoding="utf-8").splitlines():
        if hashlib.sha256(candidate.encode()).hexdigest() == digest:
            cracked = candidate
            break

    if cracked:
        write_text(cracked_path, cracked + "\n")
        print("Python dictionary attack cracked the hash:", cracked)

    john = tool_path("john")
    hashcat = tool_path("hashcat")

    if john:
        try:
            run_command(
                [
                    john,
                    "--format=Raw-SHA256",
                    "--wordlist=" + str(wordlist_path.resolve()),
                    str(hash_path.resolve()),
                ]
            )
        except RuntimeError:
            print("John command did not complete on this machine, but the lab files were created.")
    else:
        print("\nJohn the Ripper command to try:")
        print("  john --format=Raw-SHA256 --wordlist=" + str(wordlist_path) + " " + str(hash_path))

    if hashcat:
        potfile = demo_dir / "hashcat.potfile"
        hashcat_dir = Path(hashcat).resolve().parent
        try:
            run_command(
                [
                    hashcat,
                    "-m",
                    "1400",
                    "-a",
                    "0",
                    str(hash_path.resolve()),
                    str(wordlist_path.resolve()),
                    "--potfile-path",
                    str(potfile.resolve()),
                    "--quiet",
                ],
                cwd=hashcat_dir,
            )
        except RuntimeError:
            print("Hashcat command did not complete on this machine, but the lab files were created.")
    else:
        print("\nHashcat command to try:")
        print("  hashcat -m 1400 -a 0 " + str(hash_path) + " " + str(wordlist_path))


def make_netcat_payload():
    demo_dir = BASE_DIR / "netcat"
    ensure_dir(demo_dir)

    plaintext_path = demo_dir / "plain.txt"
    ciphertext_path = demo_dir / "ciphertext.txt"
    decrypted_path = demo_dir / "decrypted.txt"

    aes = AESCrypto("netcat-demo-key")
    ciphertext = aes.encrypt(MESSAGE)
    plaintext = aes.decrypt(ciphertext)

    write_text(plaintext_path, MESSAGE + "\n")
    write_text(ciphertext_path, ciphertext + "\n")
    write_text(decrypted_path, plaintext + "\n")

    return ciphertext_path, decrypted_path


def demo_netcat_guide():
    ciphertext_path, decrypted_path = make_netcat_payload()
    nc = tool_path("nc", "ncat", "netcat") or "nc"

    print("\nNetcat practical files are ready.")
    print("Ciphertext payload:", ciphertext_path)
    print("Local decrypt check:", decrypted_path)
    print("\nTerminal 1 receiver:")
    print("  " + shell_quote(nc) + " -l -p 9999 > data/tool_practical/netcat/received_ciphertext.txt")
    print("\nTerminal 2 sender:")
    print("  " + shell_quote(nc) + " 127.0.0.1 9999 < data/tool_practical/netcat/ciphertext.txt")
    print("\nWireshark filter while sending:")
    print("  tcp.port == 9999")
    print("\nExpected observation: Wireshark shows the Base64 ciphertext, not the plaintext message.")


def netcat_python_send(host, port):
    ciphertext_path, _ = make_netcat_payload()
    payload = ciphertext_path.read_bytes()
    with socket.create_connection((host, port), timeout=10) as sock:
        sock.sendall(payload)
    print("Sent encrypted payload to " + host + ":" + str(port))


def netcat_python_receive(host, port):
    demo_dir = BASE_DIR / "netcat"
    ensure_dir(demo_dir)
    received_path = demo_dir / "received_ciphertext.txt"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print("Listening on " + host + ":" + str(port))
        conn, addr = server.accept()
        with conn:
            data = conn.recv(65536)
            received_path.write_bytes(data)
            print("Received encrypted payload from", addr)
            print("Saved:", received_path)


def demo_wireshark_guide():
    demo_netcat_guide()
    print("\nWireshark is an observation tool, so this project prepares traffic for it.")
    print("Start capture on the loopback adapter, send the Netcat payload, then inspect tcp.port == 9999.")


def list_tools():
    checks = {
        "OpenSSL": tool_path("openssl"),
        "GnuPG": tool_path("gpg", "gpg2"),
        "John the Ripper": tool_path("john"),
        "Hashcat": tool_path("hashcat"),
        "Netcat": tool_path("nc", "ncat", "netcat"),
        "Wireshark": tool_path("wireshark", "tshark"),
    }

    print("Practical tool availability:")
    for name, path in checks.items():
        print("  " + name + ": " + (path if path else "not found"))


def run_all():
    list_tools()
    for demo in (demo_openssl, demo_gnupg, demo_password_attack, demo_netcat_guide, demo_wireshark_guide):
        try:
            print("\n" + "=" * 72)
            demo()
        except RuntimeError as exc:
            print("Skipped after error:", exc)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Practical study demos for OpenSSL, GnuPG, Hashcat/John, Netcat, and Wireshark."
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="Show which external tools are installed.")
    sub.add_parser("openssl", help="Run the OpenSSL key/cert/AES practical.")
    sub.add_parser("gnupg", help="Run the GnuPG sign/encrypt practical.")
    sub.add_parser("password-attack", help="Create and crack a weak SHA-256 password hash.")
    sub.add_parser("netcat", help="Prepare encrypted Netcat payload and lab commands.")
    sub.add_parser("wireshark", help="Prepare Wireshark packet-capture lab instructions.")
    sub.add_parser("all", help="Run every non-interactive practical.")

    send = sub.add_parser("socket-send", help="Python fallback sender for the Netcat practical.")
    send.add_argument("--host", default="127.0.0.1")
    send.add_argument("--port", type=int, default=9999)

    receive = sub.add_parser("socket-receive", help="Python fallback receiver for the Netcat practical.")
    receive.add_argument("--host", default="127.0.0.1")
    receive.add_argument("--port", type=int, default=9999)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        list_tools()
    elif args.command == "openssl":
        demo_openssl()
    elif args.command == "gnupg":
        demo_gnupg()
    elif args.command == "password-attack":
        demo_password_attack()
    elif args.command == "netcat":
        demo_netcat_guide()
    elif args.command == "wireshark":
        demo_wireshark_guide()
    elif args.command == "all":
        run_all()
    elif args.command == "socket-send":
        netcat_python_send(args.host, args.port)
    elif args.command == "socket-receive":
        netcat_python_receive(args.host, args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nStopped by user.")
