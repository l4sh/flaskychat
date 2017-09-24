"""
    server/app.py
    App initialization
"""
import logging
from os import environ
from flask import Flask, render_template

from .events import socketio
from .routes import main_blueprint
from .settings import Config


def init_app(config=Config):
    """
    Initialize flask application
    """
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config)

    if app.config['STANDALONE_MODE']:
        app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    socketio.run(app, host='0.0.0.0')
