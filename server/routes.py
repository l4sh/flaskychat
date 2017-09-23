"""
    server/routes.py
    Application routes
"""
from os import path
from flask import Blueprint, render_template, abort, url_for
from .settings import Config


main_blueprint = Blueprint('main',
                           __name__,
                           static_folder=Config.CLIENT_STATIC_PATH,
                           template_folder=Config.CLIENT_DIST_PATH)

@main_blueprint.route('/')
def index():
    return render_template('index.html')
