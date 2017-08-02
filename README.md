# Connect Box WiFi
Web application that lets you turn the WiFi of your Connect Box on/off.

This was developed and tested on a Raspberry Pi, so if you are working on
different platforms, some installation steps may differ as well. Certainly
the executable that you need to download in the geckodriver section is going
to be the one for your computer's CPU architecture instead of the ARM one.

Currently only the underlying script is done (so no web application really),
but the plan is to implement a nice on/off switch using Flask.

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
sudo pip install Virtualenv
```
Then, inside the project directory do
```
virtualenv venv         # Create venv
. venv/bin/activate     # Activate venv
pip install -e .        # Install dependencies from setup.py
deactivate              # Deactivate venv
```
Remember: every time you want to run the script, start the Virtualenv with
```
. venv/bin/activate
```
and to deactivate it once you're done, just type
`deactivate`.

## Usage
With the activated Virtualenv and inside the project directory, run
```
python control.py -p <password> -a 1
```
to turn WiFi on and
```
python control.py -p <password> -a 0
```
to turn it off.
