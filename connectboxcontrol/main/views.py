from flask import Blueprint, render_template, request, url_for
from connectboxcontrol.util.control import control
import os
import json
import threading

main_blueprint = Blueprint('main', __name__, static_folder='static',
                           static_url_path='/main/static',
                           template_folder='templates')

@main_blueprint.route('/', methods=['GET'])
def main_get():
    """Show the main page with the on/off button."""
    return render_template('main.html')

@main_blueprint.route('/', methods=['POST'])
def main_post():
    """Turn the WiFi on/off."""
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
            password = config['password']
        if 'on' in request.form:
            threading.Thread(target=control, args=(password, 1)).start()
            return render_template(
                'message.html',
                title="Success",
                message="WiFi is being turned on."
            )
        elif 'off' in request.form:
            threading.Thread(target=control, args=(password, 0)).start()
            return render_template(
                'message.html',
                title="Success",
                message="WiFi is being turned off."
            )
    else:
        url = url_for('config.config_get', _external=True)
        return render_template(
            'message.html',
            title="Error",
            message=("The router password is unknown.<br/>Set it up "
                     "<a href='" + url + "'>here</a>.")
        )
