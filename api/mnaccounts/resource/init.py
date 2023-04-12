"""Init database."""

from flask_restful import Resource

from .. import db

class InitResource(Resource):
    def put(self):
        db.reset()
        return {
            'data': None
        }


class RefreshResource(Resource):
    def put(self):
        db.refresh()
        return {
            'data': None
        }
