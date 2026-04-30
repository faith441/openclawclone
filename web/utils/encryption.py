"""
Encryption utilities for sensitive data (API keys, credentials)
"""
from cryptography.fernet import Fernet
import base64
from flask import current_app


def get_encryption_key():
    """Get encryption key from config"""
    key = current_app.config['ENCRYPTION_KEY']
    # Ensure key is 32 bytes and base64 encoded
    if len(key) == 64:  # Hex string
        key_bytes = bytes.fromhex(key)[:32]
    else:
        key_bytes = key.encode()[:32]
    return base64.urlsafe_b64encode(key_bytes)


def encrypt(plaintext):
    """
    Encrypt plaintext string

    Args:
        plaintext (str): Text to encrypt

    Returns:
        str: Encrypted text (base64 encoded)
    """
    if not plaintext:
        return None

    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(plaintext.encode())
    return encrypted.decode()


def decrypt(ciphertext):
    """
    Decrypt ciphertext string

    Args:
        ciphertext (str): Encrypted text

    Returns:
        str: Decrypted plaintext
    """
    if not ciphertext:
        return None

    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted = f.decrypt(ciphertext.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None


def encrypt_dict(data):
    """
    Encrypt sensitive fields in a dictionary

    Args:
        data (dict): Dictionary with sensitive fields

    Returns:
        dict: Dictionary with encrypted values
    """
    if not data:
        return {}

    encrypted_data = {}
    sensitive_keys = ['api_key', 'secret', 'password', 'token', 'client_secret']

    for key, value in data.items():
        # Check if key contains sensitive words
        is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_keys)

        if is_sensitive and isinstance(value, str) and value:
            encrypted_data[key] = encrypt(value)
        else:
            encrypted_data[key] = value

    return encrypted_data


def decrypt_dict(data):
    """
    Decrypt sensitive fields in a dictionary

    Args:
        data (dict): Dictionary with encrypted fields

    Returns:
        dict: Dictionary with decrypted values
    """
    if not data:
        return {}

    decrypted_data = {}
    sensitive_keys = ['api_key', 'secret', 'password', 'token', 'client_secret']

    for key, value in data.items():
        # Check if key contains sensitive words
        is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_keys)

        if is_sensitive and isinstance(value, str) and value:
            decrypted_data[key] = decrypt(value)
        else:
            decrypted_data[key] = value

    return decrypted_data
