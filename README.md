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
### Development server (simple)
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
device in the browser, and the configuration interface to enter the router
password is located at <IP>/config.

### Gunicorn & Nginx (less simple but better)
First, you're going to want to make sure to have Nginx installed.
```
sudo apt-get install nginx
```
No need to worry about Gunicorn, as it's a dependency that was already
installed with setup.py. Next, you may want to create a systemd service that
starts the Gunicorn instance at boot. There is already a service file
prepared, called `connectboxcontrol.service`. Check it out, as you may need
to change the username or the path where your project is located. After that,
you're ready to copy the file to the systemd directory and enable the service.
```
sudo cp connectboxcontrol.service /etc/systemd/system/
sudo systemctl start connectboxcontrol
sudo systemctl enable connectboxcontrol
```
Next, we'll set up Nginx. As before, the file `nginx_config` is all you need.
Open it and add the IP of your device at the appropriate location. Then you
can copy the file to where it needs to be, create a symlink for Nginx, test
for syntax errors and restart the Nginx service.
```
sudo cp nginx_config /etc/nginx/sites-available/connectboxcontrol
sudo ln -s /etc/nginx/sites-available/connectboxcontrol /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
And that's it. You should now be able to find the main page by typing in the
IP of your device in the browser, and the configuration interface to enter the
router password is located at <IP>/config.
