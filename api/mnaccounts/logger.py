"""Logger."""
import sys
import os

import logging
import logging.config
import flask.logging

class StdoutHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)

def init(app):
    if not 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        logging.config.dictConfig(app.config['LOGGING'])

def get_logger(name=None):
    return logging.getLogger(name)

