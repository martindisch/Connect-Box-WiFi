import argparse
import json
import requests
import sys
from connectboxcontrol.util import crypto
from connectboxcontrol.util.crypto import hex


def login(password, salt, iv, key):
    """Start a new session.

    Parameters
    ----------
    password : str
        The password
    salt : bytes
        The salt
    iv : bytes
        The IV
    key : bytes
        The key

    Returns
    -------
    tuple of str
        The php_sessid, csrf_nonce pair

    """
    # Prepare our package for logging in
    config_data = {
        'csrfNonce': "undefined",
        'newPassword': password,
        'oldPassword': password,
        'ChangePassword': "false",
        'authData': "encryptData",
        'salt': hex(salt),
        'iv': hex(iv)
    }
    # Encrypt it
    config_blob = crypto.ccm_encrypt(
        key,
        iv,
        json.dumps(config_data),
        config_data['authData'])
    # And put it into the structure we're going to send
    encrypted_config_data = {
        'encryptedBlob': config_blob,
        'salt': hex(salt),
        'iv': hex(iv),
        'authData': config_data['authData'],
    }
    login_body_to_send = {
        'configInfo': json.dumps(encrypted_config_data)
    }

    # Now we can make the request to initiate the session
    r = requests.post(
        "http://192.168.0.1/php/ajaxSet_Password.php",
        data=login_body_to_send)
    # Fetch useful parts from the response
    php_sessid = r.cookies['PHPSESSID']
    body = r.json()
    p_status = body['p_status']
    if p_status == "MisMatch":
        raise Exception("Login mismatch, maybe the password is incorrect?")
    csrf_nonce = body['nonce']

    return php_sessid, csrf_nonce


def switch_wifi(salt, iv, key, php_sessid, csrf_nonce, action):
    """Enable or disable the WiFi.

    Parameters
    ----------
    salt : bytes
        The salt
    iv : bytes
        The IV
    key : bytes
        The key
    php_sessid : str
        The PHP session ID
    csrf_nonce : str
        The CSRF token for the session
    action : int
        Whether to turn WiFi on (1) or off (0)

    """
    # Prepare the package for changing the WiFi state
    wifi_data = {
        'js_24g_stat': "false" if action == 0 else "true",
        'js_24g_channel_mode': "false",
        'js_24g_channelBW': "20MHz",
        'js_24g_mode': "g,n",
        'js_24g_channel': 11,
        'js_5g_stat': "false",
        'js_5g_mode': "a,n,ac",
        'js_5g_channel_mode': "false",
        'js_5g_channel': 44,
        'js_5g_channelBW': "80MHz",
        'csrf_nonce': csrf_nonce,
        'authData': "encryptData",
        'salt': hex(salt),
        'iv': hex(iv)
    }
    # Encrypt it
    wifi_blob = crypto.ccm_encrypt(
        key,
        iv,
        json.dumps(wifi_data),
        wifi_data['authData'])
    # And put it into the structure we're going to send
    encrypted_wifi_data = {
        'encryptedBlob': wifi_blob,
        'salt': hex(salt),
        'iv': hex(iv),
        'authData': wifi_data['authData'],
    }
    wifi_body_to_send = {
        'wifiData': json.dumps(encrypted_wifi_data),
        'opType': "WRITE"
    }

    # Make the request to change the settings
    r = requests.post(
        "http://192.168.0.1/php/wifi_data.php",
        data=wifi_body_to_send,
        headers={
            'Origin': "http://192.168.0.1",
            'CSRF_NONCE': csrf_nonce
        },
        cookies={
            'PHPSESSID': php_sessid
        })
    if r.text != "\nUpdated successfully":
        raise Exception("Failed to update successfully")


def control(password, action=0):
    """Turn WiFi on or off.

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

    print("Logging in")
    php_sessid, csrf_nonce = login(password, salt, iv, key)

    print("Turning WiFi " + ("off" if action == 0 else "on"))
    switch_wifi(salt, iv, key, php_sessid, csrf_nonce, action)


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
