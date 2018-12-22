import argparse
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
    # Additional timeout for Selenium to be safe
    timeout = 2
    # Prepare Xvfb display
    print("Preparing display")
    display = Display(visible=0, size=(800, 600))
    display.start()
    # Instantiate browser and visit login page
    print("Starting browser")
    browser = webdriver.Firefox()
    wait = ui.WebDriverWait(browser, 60)
    browser.get('http://192.168.0.1/common_page/login.html')

    # Fill out login form and submit
    print("Logging in")
    login_pw = wait.until(EC.element_to_be_clickable((By.ID, 'loginPassword')))
    time.sleep(timeout)
    login_pw.send_keys(password)
    continue_button = wait.until(EC.element_to_be_clickable((By.ID, 'c_42')))
    time.sleep(timeout)
    continue_button.click()

    # Find the WiFi settings and load the page
    print("Opening WiFi settings")
    adv_settings = wait.until(EC.element_to_be_clickable((By.ID, 'c_mu05')))
    time.sleep(timeout)
    adv_settings.click()
    wifi_settings = wait.until(EC.element_to_be_clickable((By.ID, 'c_mu06')))
    time.sleep(timeout)
    wifi_settings.click()
    wifi_page = wait.until(EC.element_to_be_clickable((By.ID, 'c_mu07')))
    time.sleep(timeout)
    wifi_page.click()
    # Give the page time to load completely (checkbox won't work otherwise)
    time.sleep(5)

    # Select 2.4 GHz on/off checkbox and apply settings
    if action == 1:
        print("Turning WiFi on")
        on = wait.until(EC.element_to_be_clickable((By.ID, 'iwlanRadio2G1')))
        time.sleep(timeout)
        on.click()
    elif action == 0:
        print("Turning WiFi off")
        off = wait.until(EC.element_to_be_clickable((By.ID, 'iwlanRadio2G2')))
        time.sleep(timeout)
        off.click()

    # Apply settings
    apply = wait.until(EC.element_to_be_clickable((By.ID, 'c_02')))
    time.sleep(timeout)
    apply.click()
    # Wait until settings are applied (checkboxes clickable again)
    wait.until(EC.element_to_be_clickable((By.ID, 'iwlanRadio2G1')))

    # Logout
    print("Logging out")
    logout = wait.until(EC.element_to_be_clickable((By.ID, 'c_mu30')))
    logout.click()
    # Wait until logout process complete (password input clickable)
    wait.until(EC.element_to_be_clickable((By.ID, 'loginPassword')))

    # Close browser instance
    print("Terminating browser")
    browser.quit()

    # Stop virtual display
    print("Stopping display")
    display.popen.terminate()


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
