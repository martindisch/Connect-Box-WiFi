import argparse
import json
import requests
import sys
from connectboxcontrol.util import crypto


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
    salt, iv = crypto.generate_salt_iv()
    # And a derived key too
    key = crypto.derive_key(password, salt)

    # Then we need to prepare our package for logging in
    config_data = {
        'csrfNonce': "undefined",
        'newPassword': password,
        'oldPassword': password,
        'ChangePassword': "false",
        'authData': "encryptData",
        'salt': salt.hex(),
        'iv': iv.hex()
    }
    # Encrypt it
    blob = crypto.ccm_encrypt(
        key,
        iv,
        json.dumps(config_data),
        config_data['authData'])
    # And put it into the structure we're going to send
    encrypted_config_data = {
        'encryptedBlob': blob,
        'salt': salt.hex(),
        'iv': iv.hex(),
        'authData': config_data['authData'],
    }
    body_to_send = {
        'configInfo': json.dumps(encrypted_config_data)
    }

    # Now we can make the request to initiate the session
    r = requests.post(
        "http://192.168.0.1/php/ajaxSet_Password.php",
        data=body_to_send)
    # Fetch useful parts from the response
    php_sessid = r.cookies['PHPSESSID']
    body = r.json()
    p_status = body['p_status']
    if p_status == "MisMatch":
        sys.exit("Login mismatch, maybe the password is incorrect?")
    csrf_nonce = body['nonce']


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
