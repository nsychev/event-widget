import os

import flask

from werkzeug.middleware.proxy_fix import ProxyFix

from . import blueprints
from .config import load_config
from .storage.utils import install_database


def create_app():
    app = flask.Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
    app.config.from_mapping(load_config(os.path.dirname(app.root_path)))
    install_database(app)

    app.register_blueprint(blueprints.coffee)

    return app
