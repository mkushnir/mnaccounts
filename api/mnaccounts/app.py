"""App."""

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

import mnaccounts.db
import mnaccounts.logger
import mnaccounts.account

from .utils import MyJSONEncoder

from .resource.simple import (
    FlaskUserResource,
    DbAuditResource,
    UserResource,
    TargetResource,
    PolicyResource,
    UserTargetPolicyResource,
    TicketResource,
)

from .resource.init import InitResource
from .resource.version import VersionResource

app = Flask(__name__)
app.config.from_envvar('MNACCOUNTS_APP_CONFIG_FILE')
mnaccounts.logger.init(app)
app.config['RESTFUL_JSON'] = {
    'cls': MyJSONEncoder,
}

mnaccounts.db.init()

mnaccounts.account.init(app)

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

api.add_resource(InitResource, '/v1/init')
api.add_resource(VersionResource, '/v1/version')

#api.add_resource(FlaskUserResource, '/v1/flaskuser', '/v1/flaskuser/<int:id>')
#api.add_resource(DbAuditResource, '/v1/dbaudit', '/v1/dbaudit/<int:id>')
api.add_resource(UserResource, '/v1/user', '/v1/user/<int:id>')
api.add_resource(TargetResource, '/v1/target', '/v1/target/<int:id>')
api.add_resource(PolicyResource, '/v1/policy', '/v1/policy/<int:id>')
api.add_resource(UserTargetPolicyResource, '/v1/user_target_policy', '/v1/user_target_policy/<int:id>')
api.add_resource(TicketResource, '/v1/ticket', '/v1/ticket/<int:id>')
