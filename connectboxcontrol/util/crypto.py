import secrets
import hashlib
from Crypto.Cipher import AES


PBKDF2_ITERATIONS = 1000
PBKDF2_KEYSIZE_BYTES = 16
CCM_TAGLENGTH_BYTES = 16;


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


def ccm_encrypt(key, iv, plain_text, authenticated_data):
    """Encrypt & authenticate data.

    Parameters
    ----------
    key : bytes
        The key
    iv : bytes
        The IV
    plain_text : str
        The data to encrypt
    authenticated_data : str
        The data to authenticate

    Returns
    -------
    str
        The ciphertext & tag concatenated in hex representation

    """
    cipher = AES.new(key, AES.MODE_CCM, nonce=iv, mac_len=CCM_TAGLENGTH_BYTES)
    cipher.update(authenticated_data.encode())
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
    return f"{ciphertext.hex()}{tag.hex()}"


def ccm_decrypt(key, iv, blob, authenticated_data):
    """Decrypt & authenticate data.

    Parameters
    ----------
    key : bytes
        The key
    iv : bytes
        The IV
    blob : str
        The ciphertext & tag concatenated in hex representation
    authenticated_data : str
        The data to authenticate

    Returns
    -------
    str
        The plaintext

    """
    cipher = AES.new(key, AES.MODE_CCM, nonce=iv, mac_len=CCM_TAGLENGTH_BYTES)
    cipher.update(authenticated_data.encode())
    blob_bytes = bytes.fromhex(blob)
    ciphertext = blob_bytes[:-CCM_TAGLENGTH_BYTES]
    tag = blob_bytes[-CCM_TAGLENGTH_BYTES:]
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()
