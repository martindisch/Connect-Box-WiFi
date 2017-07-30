import argparse
from selenium import webdriver
import time

def control(password, action=0):
    """Visit the router's configuration page and turn WiFi on or off.

    Parameters
    ----------
    password : str
        The password to login with
    action : int, optional
        Whether to turn WiFi on (1) or off (0)
    """
    # Instantiate browser and visit login page
    browser = webdriver.Firefox()
    browser.get('http://192.168.0.1/common_page/login.html')
    time.sleep(5)

    # Fill out login form and submit
    loginPassword = browser.find_element_by_id('loginPassword')
    loginPassword.send_keys(password)
    continueButton = browser.find_element_by_id('c_42')
    continueButton.click()
    time.sleep(5)

    # Find the WiFi settings and load the page
    advancedSettings = browser.find_element_by_id('c_mu05')
    advancedSettings.click()
    wifiSettings = browser.find_element_by_id('c_mu06')
    wifiSettings.click()
    wifiPage = browser.find_element_by_id('c_mu07')
    wifiPage.click()
    time.sleep(5)

    # Select 2.4 GHz on/off checkbox and apply settings
    if action == 1:
        on24 = browser.find_element_by_id('iwlanRadio2G1')
        on24.click()
    elif action == 0:
        off24 = browser.find_element_by_id('iwlanRadio2G2')
        off24.click()
    applyButton = browser.find_element_by_id('c_02')
    applyButton.click()
    time.sleep(5)

    # Logout
    logout = browser.find_element_by_id('c_mu30')
    logout.click()
    time.sleep(5)

    # Close browser instance
    browser.quit()

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
