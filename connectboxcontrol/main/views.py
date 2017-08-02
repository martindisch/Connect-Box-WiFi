from flask import Blueprint, render_template, request
from connectboxcontrol.util import control

main_blueprint = Blueprint('main', __name__, static_folder='static',
                           static_url_path='/main/static',
                           template_folder='templates')

@main_blueprint.route('/', methods=['GET'])
def main_get():
    """Show the main page with the on/off button."""
    return render_template('main.html')
