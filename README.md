# Connect Box WiFi
Web application that lets you turn the WiFi of your Connect Box on/off.

This was developed and tested on a Raspberry Pi, so if you are working on
different platforms, some installation steps may differ as well. Certainly
the executable that you need to download in the geckodriver section is going
to be the one for your computer's CPU architecture instead of the ARM one.

## Installation
### Firefox
We're going to use Firefox as a browser, because the Chrome webdriver is
not available for ARM anymore.
```
sudo apt-get install firefox-esr
```
Since selenium is going to open actual browser windows, you need to run
everything inside a graphical environment.

### geckodriver
Selenium needs the latest geckodriver, so you'll have to install that too.
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-arm7hf.tar.gz
tar -xvzf geckodriver-v0.18.0-arm7hf.tar.gz
rm geckodriver-v0.18.0-linux64.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```

### Xvfb
Because you may want to run this on a Raspberry Pi you don't always have a
display attached to, we need this package together with PyVirtualDisplay to
make it run.
```
sudo apt-get install xvfb
```
PyVirtualDisplay is going to be automatically installed by setup.py in the next
step.

### venv/Python dependencies
Because there is a Python module to install (selenium), it's recommended to set
up a Virtualenv for that.
```
sudo pip install virtualenv
```
Then, inside the project directory do
```
virtualenv -p python3 venv  # Create venv
. venv/bin/activate         # Activate venv
pip install -e .            # Install dependencies from setup.py
deactivate                  # Deactivate venv
```

## Usage
### Development server (easy)
Flask has a built-in development server. While very convenient, it's generally
not recommended to run your app with this method in production. For one, even
with debug mode disabled, it's not the most performant or secure way of running
your app. Another problem is that if you want it to run on port 80, you'll have
to `sudo` the application and giving your potentially insecure webserver that
privilege can be dangerous.
But since you're going to be running the system inside your (hopefully)
protected LAN, this might be acceptable in just this special case.
If you think so, all you need to do is run the start script.
```
sudo ./start80.sh
```
With that, the main on/off interface can be reached by typing in the IP of your
Pi in the browser, and the configuration interface to enter the router
password is located at <IP>/config.
