# Connect Box WiFi
Web application that lets you turn the WiFi of your Connect Box on/off.

## Installation
### Firefox
We're going to use Firefox as a browser, although you could easily rewrite
the script for whichever one you like best or already have installed.
```
sudo apt-get install firefox-esr
```
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
