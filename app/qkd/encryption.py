### AES Encryption with Shared Key

import base64, hashlib
from cryptography.fernet import Fernet

def convert_key_to_fernet_format(bit_key):
    """
        Converts a list of bits into a Fernet-compatible key
    """
    bit_str = ''.join(str(b) for b in bit_key)
    sha = hashlib.sha256(bit_str.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt_message(message, key):
    """
        Encrypt a plaintext message using the shared Fernet key.
    """
    fernet_key = convert_key_to_fernet_format(key)
    fernet = Fernet(fernet_key)
    return fernet.encrypt(message.encode())

def decrypt_message(ciphertext, key):
    """
        Decrypt the ciphertext back into plaintext using the Fernet key.
    """
    fernet_key = convert_key_to_fernet_format(key)
    fernet = Fernet(fernet_key)
    return fernet.decrypt(ciphertext).decode()
