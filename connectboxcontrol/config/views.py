from flask import Blueprint, render_template, request
import os
import json

config_blueprint = Blueprint('config', __name__, static_folder='static',
                             static_url_path='/config/static',
                             template_folder='templates')

@config_blueprint.route('/config', methods=['GET'])
def config_get():
    """Show the configuration page for the password."""
    return render_template('config.html')
    
@config_blueprint.route('/config', methods=['POST'])
def config_post():
    """Save the given password and show the configuration page."""
    password = request.form['password']
    with open('config.json', 'w') as f:
        json.dump({'password': password}, f)
    title = "Success"
    message = "The password has been saved."
    return render_template('success.html',
                           password=password, message=message, title=title)
