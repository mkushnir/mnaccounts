"""Init database."""

from flask_restful import Resource

from .. import db

class InitResource(Resource):
    def put(self):
        db.reset()
