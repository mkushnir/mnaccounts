"""Version."""
from flask_restful import Resource

import mnaccounts.version

import mnaccounts.resource

class VersionResource(Resource):
    method_decorators = {
        'get': [
            mnaccounts.resource.mnerror,
            mnaccounts.resource.mnaccess_policy,
            mnaccounts.resource.login_required,
        ],
    }
    def get(self):
        return {
            'data': {
                'short': mnaccounts.version._version,
                'long': mnaccounts.version._version_long,
            },
        }
