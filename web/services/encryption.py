"""
Encryption service for securely storing API keys
"""
from cryptography.fernet import Fernet
import os
import base64
import hashlib

# Get encryption key from environment or generate one
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    # Generate a key from app secret for consistent encryption
    secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Derive a Fernet-compatible key from the secret
    key_material = hashlib.sha256(secret_key.encode()).digest()
    ENCRYPTION_KEY = base64.urlsafe_b64encode(key_material)

fernet = Fernet(ENCRYPTION_KEY)


def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt an API key for secure storage

    Args:
        api_key: The plain text API key

    Returns:
        Encrypted API key as base64 string
    """
    if not api_key:
        raise ValueError("API key cannot be empty")

    encrypted = fernet.encrypt(api_key.encode())
    return encrypted.decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt an API key for use

    Args:
        encrypted_key: The encrypted API key

    Returns:
        Plain text API key
    """
    if not encrypted_key:
        raise ValueError("Encrypted key cannot be empty")

    decrypted = fernet.decrypt(encrypted_key.encode())
    return decrypted.decode()
