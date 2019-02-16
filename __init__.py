import logging
import os
from flask import Flask


def create_app():
    app = Flask("chandelier", instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello, world!"

    from . import db
    db.init_app(app)

    from .api import api_projects_bp
    app.register_blueprint(api_projects_bp)

    return app
