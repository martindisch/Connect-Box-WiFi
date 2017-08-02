from flask import Flask
from .main.views import main_blueprint
from .config.views import config_blueprint

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.register_blueprint(config_blueprint)
