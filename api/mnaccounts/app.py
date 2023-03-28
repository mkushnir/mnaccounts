"""App."""

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

import mnaccounts.db
import mnaccounts.logger
import mnaccounts.login

from .utils import MyJSONEncoder

app = Flask(__name__)
app.config.from_envvar('MNACCOUNTS_APP_CONFIG_FILE')
mnaccounts.logger.init(app)
app.config['RESTFUL_JSON'] = {
    'cls': MyJSONEncoder,
}

mnaccounts.db.init()

mnaccounts.login.init(app)

cors = CORS(
    app,
    resources={
        '/*': {
            'origins': [
                'https://mkushnir.mooo.com:8912',
                'https://mkushnir.mooo.com:8914',
                'https://accounts.google.com',
            ],
            'supports_credentials': True,
        }
    },
)

api = Api(app)
