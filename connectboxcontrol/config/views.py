from flask import Blueprint, render_template, request

config_blueprint = Blueprint('config', __name__, static_folder='static',
                             static_url_path='/config/static',
                             template_folder='templates')

@config_blueprint.route('/config', methods=['GET'])
def main_get():
    """Show the configuration page for the password."""
    return render_template('config.html')
