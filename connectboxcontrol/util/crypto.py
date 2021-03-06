import hashlib
import codecs
from Crypto.Cipher import AES
import Crypto.Random as random


PBKDF2_ITERATIONS = 1000
PBKDF2_KEYSIZE_BYTES = 16
CCM_TAGLENGTH_BYTES = 16


def hex(b):
    """Convert the given bytes to hexadecimal string representation.

    Parameters
    ----------
    b : bytes
        The byte string to convert

    Returns
    -------
    str
        Hexadecimal string

    """
    return codecs.encode(b, "hex").decode("ascii")


def generate_salt_iv():
    """Generate a salt & IV pair.

    Returns
    -------
    tuple of two bytes
        The salt and IV

    """
    return random.get_random_bytes(8), random.get_random_bytes(8)


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
    return hex(ciphertext) + hex(tag)
