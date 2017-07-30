# Connect Box WiFi
Web application that lets you turn the WiFi of your Connect Box on/off.

Currently only the underlying script is done (so no web application really),
but the plan is to implement a nice on/off switch using Flask.

## Installation
### Firefox
We're going to use Firefox as a browser, although you could easily rewrite
the script for whichever one you like best or already have installed.
```
sudo apt-get install firefox-esr
```
Since selenium is going to open actual browser windows, you need to run
everything inside a graphical environment.

### geckodriver
Since Selenium needs the latest geckodriver, you'll have to install that by
yourself.
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar -xvzf geckodriver-v0.18.0-linux64.tar.gz
rm geckodriver-v0.18.0-linux64.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```

### venv
Since there is a Python module to install (selenium), it's recommended to do
that inside a Virtualenv.
```
sudo pip install Virtualenv
```
Then, inside the project directory do
```
virtualenv venv
. venv/bin/activate     # Activate venv
pip install selenium
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
to turn WiFi on and run it with `-a 0` to turn it off.
