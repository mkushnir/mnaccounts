"""Init database."""

from flask_restful import Resource

from .. import db

import mnaccounts.resource

class InitResource(Resource):
    method_decorators = {
        'put': [
            mnaccounts.resource.mnerror,
            mnaccounts.resource.mnaccess_policy,
            mnaccounts.resource.login_required,
        ],
    }
    def put(self):
        db.reset()
        return {
            'data': None
        }


class RefreshResource(Resource):
    method_decorators = {
        'put': [
            mnaccounts.resource.mnerror,
            mnaccounts.resource.mnaccess_policy,
            mnaccounts.resource.login_required,
        ],
    }
    def put(self):
        db.refresh()
        return {
            'data': None
        }
