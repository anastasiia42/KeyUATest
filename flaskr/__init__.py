import os

from flask import (Flask, redirect, render_template, request, session, url_for)
from flask_socketio import SocketIO


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    @app.route("/")
    def run():
        return redirect(url_for('auth.login'))

    from . import db
    db.init_app(app)

    from . import auth, weather
    app.register_blueprint(auth.bp)
    app.register_blueprint(weather.bp)
    app.add_url_rule('/', endpoint='index')

    return app
