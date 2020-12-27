import secrets
import hashlib


PBKDF2_ITERATIONS = 1000
PBKDF2_KEYSIZE_BYTES = 16


def generate_salt_iv():
    """Generate a salt & IV pair.

    Returns
    -------
    tuple of two bytes
        The salt and IV

    """
    return secrets.token_bytes(8), secrets.token_bytes(8)


def derive_key(password, salt):
    """Derive a key based on password & salt.

    Parameters
    ----------
    password : str
        The password to use in key derivation
    salt : bytes
        The salt to use in key derivation

    Returns
    -------
    bytes
        The key

    """
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        PBKDF2_ITERATIONS,
        PBKDF2_KEYSIZE_BYTES)
    return dk
