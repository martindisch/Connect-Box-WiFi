import argparse
import secrets
import hashlib


PBKDF2_ITERATIONS = 1000
PBKDF2_KEYSIZE_BYTES = 16


def generate_salt_iv():
    """Return a newly generated salt & IV.

    Returns
    -------
    tuple of two str
        The salt and IV

    """
    return secrets.token_hex(8), secrets.token_hex(8)


def control(password, action=0):
    """Visit the router's configuration page and turn WiFi on or off.

    Parameters
    ----------
    password : str
        The password to login with
    action : int, optional
        Whether to turn WiFi on (1) or off (0)

    """
    # For encrypting our data, we first need a salt & IV
    salt, iv = generate_salt_iv()
    # And a derived key too
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        PBKDF2_ITERATIONS,
        PBKDF2_KEYSIZE_BYTES)
    key = dk.hex()
    print(key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn WiFi on/off.")
    parser.add_argument(
        '--password', '-p', help="The router login password", required=True
    )
    parser.add_argument(
        '--action', '-a', type=int,
        help="Action: Turn on (1) or off (0)", required=True
    )
    args = parser.parse_args()
    control(args.password, args.action)
