import argparse
from selenium import webdriver
from pyvirtualdisplay import Display
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
    # Prepare Xvfb display
    print("Preparing display")
    display = Display(visible=0, size=(800, 600))
    display.start()
    # Set up capabilities to make it run with Firefox ESR
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = False
    # Instantiate browser and visit login page
    print("Starting browser")
    browser = webdriver.Firefox(capabilities=caps)
    browser.get('http://192.168.0.1/common_page/login.html')
    time.sleep(5)

    # Fill out login form and submit
    print("Logging in")
    loginPassword = browser.find_element_by_id('loginPassword')
    loginPassword.send_keys(password)
    continueButton = browser.find_element_by_id('c_42')
    continueButton.click()
    time.sleep(5)

    # Find the WiFi settings and load the page
    print("Opening WiFi settings")
    advancedSettings = browser.find_element_by_id('c_mu05')
    advancedSettings.click()
    wifiSettings = browser.find_element_by_id('c_mu06')
    wifiSettings.click()
    wifiPage = browser.find_element_by_id('c_mu07')
    wifiPage.click()
    time.sleep(5)

    # Select 2.4 GHz on/off checkbox and apply settings
    if action == 1:
        print("Turning WiFi on")
        on24 = browser.find_element_by_id('iwlanRadio2G1')
        on24.click()
    elif action == 0:
        print("Turning WiFi off")
        off24 = browser.find_element_by_id('iwlanRadio2G2')
        off24.click()
    applyButton = browser.find_element_by_id('c_02')
    applyButton.click()
    time.sleep(5)

    # Logout
    print("Logging out")
    logout = browser.find_element_by_id('c_mu30')
    logout.click()
    time.sleep(5)

    # Close browser instance
    print("Terminating browser")
    browser.quit()
    
    # Stop virtual display
    print("Stopping display")
    display.stop()

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
