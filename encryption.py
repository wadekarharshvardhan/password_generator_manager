"""
encryption.py
-------------
SecureVault – Advanced Password Generator and Manager
SynthBay Solutions | Founder: Harshvardhan Wadekar

Handles AES-256 encryption and decryption of passwords using the
cryptography library's Fernet symmetric encryption scheme.

Key Derivation:
    The master password is hashed with SHA-256 and base64-encoded
    to produce a valid 32-byte Fernet key, which is AES-256 compatible.
"""

import hashlib
import base64

from cryptography.fernet import Fernet, InvalidToken


def derive_key_from_master(master_password: str) -> bytes:
    """
    Derive a 32-byte AES-256 compatible Fernet key from the master password.

    Process:
        1. Encode the master password to UTF-8 bytes.
        2. Apply SHA-256 hashing → produces a 32-byte digest.
        3. Base64-URL-encode the digest → valid Fernet key format.

    Args:
        master_password (str): The user's master password string.

    Returns:
        bytes: A 32-byte, base64-url-encoded Fernet key.
    """
    # SHA-256 produces exactly 32 bytes — perfect for AES-256
    password_bytes = master_password.encode("utf-8")
    sha256_hash = hashlib.sha256(password_bytes).digest()

    # Fernet requires keys to be URL-safe base64-encoded 32-byte values
    fernet_key = base64.urlsafe_b64encode(sha256_hash)
    return fernet_key


def encrypt_password(plain_text: str, master_password: str) -> str:
    """
    Encrypt a plaintext password using AES-256 (Fernet).

    Args:
        plain_text (str): The password to be encrypted.
        master_password (str): The master password used to derive the key.

    Returns:
        str: The encrypted password as a UTF-8 decoded string (base64 token).

    Raises:
        ValueError: If plain_text or master_password is empty.
    """
    if not plain_text:
        raise ValueError("Password to encrypt cannot be empty.")
    if not master_password:
        raise ValueError("Master password cannot be empty.")

    key = derive_key_from_master(master_password)
    fernet = Fernet(key)

    # Encrypt the password bytes → returns a signed, timestamped Fernet token
    encrypted_bytes = fernet.encrypt(plain_text.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")  # Store as string in the database


def decrypt_password(cipher_text: str, master_password: str) -> str:
    """
    Decrypt a Fernet-encrypted password back to plaintext.

    Args:
        cipher_text (str): The encrypted password token (string).
        master_password (str): The master password used during encryption.

    Returns:
        str: The decrypted plaintext password.

    Raises:
        ValueError: If the master password is incorrect or token is corrupted.
    """
    if not cipher_text:
        raise ValueError("Cipher text cannot be empty.")
    if not master_password:
        raise ValueError("Master password cannot be empty.")

    key = derive_key_from_master(master_password)
    fernet = Fernet(key)

    try:
        decrypted_bytes = fernet.decrypt(cipher_text.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except InvalidToken:
        # Raised when the key doesn't match or data is tampered with
        raise ValueError("Decryption failed: Invalid master password or corrupted data.")
