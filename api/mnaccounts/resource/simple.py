"""Simple db access."""

from ..model.flaskuser import FlaskUser
from ..model.dbaudit import DbAudit

from ..model.user import User
from ..model.target import Target
from ..model.policy import Policy
from ..model.user_target_policy import UserTargetPolicy
from ..model.user_target import UserTarget
from ..model.ticket import Ticket

from . import SimpleResource


class FlaskUserResource(SimpleResource):
    _model = FlaskUser

    def _prepare_args(self, req, args):
        from ..account import bcrypt

        if 'password' in req.json:
            args['hash'] = bcrypt.generate_password_hash(req.json['password'])
        return args


class DbAuditResource(SimpleResource):
    _model = DbAudit


class UserResource(SimpleResource):
    _model = User

    def _prepare_args(self, req, args):
        from ..account import bcrypt

        if 'password' in req.json:
            args['hash'] = bcrypt.generate_password_hash(req.json['password'])
        return args


class TargetResource(SimpleResource):
    _model = Target


class PolicyResource(SimpleResource):
    _model = Policy


class UserTargetPolicyResource(SimpleResource):
    _model = UserTargetPolicy


class UserTargetResource(SimpleResource):
    _model = UserTarget


class TicketResource(SimpleResource):
    _model = Ticket
