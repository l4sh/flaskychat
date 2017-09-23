"""
    server/settings.py
    Application config
"""
from os import environ, path, pardir
from .utils import string_to_bool


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY', 'secretkey')
    APP_DIR = path.abspath(path.dirname(__file__))
    APP_ROOT = path.abspath(path.join(APP_DIR, pardir))
    STANDALONE_MODE = string_to_bool(environ.get('STANDALONE_MODE', 'True'))

    # Client relative paths
    CLIENT_RSTATIC_PATH = environ.get('CLIENT_RSTATIC_PATH',
                                      'client/dist/static')
    CLIENT_RDIST_PATH = environ.get('CLIENT_RDIST_PATH',
                                    'client/dist')
    # Client full path
    CLIENT_STATIC_PATH = environ.get('CLIENT_STATIC_PATH',
                                     path.join(APP_ROOT, CLIENT_RSTATIC_PATH))
    CLIENT_DIST_PATH = environ.get('CLIENT_DIST_PATH',
                                   path.join(APP_ROOT, CLIENT_RDIST_PATH))
