"""Simple db access."""
import re

import flask
from flask_login import current_user
from flask_restful import abort

from ..model.flaskuser import FlaskUser
from ..model.dbaudit import DbAudit

from ..model.user import User
from ..model.target import Target
from ..model.policy import Policy
from ..model.user_target_policy import UserTargetPolicy
from ..model.user_target import UserTarget
from ..model.ticket import Ticket

from . import SimpleResource

from mnaccounts.policy import policy_validation

_re_spaces = re.compile(r'\s+')

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

    def _prepare_args(self, req, args):
        user_ = current_user
        session_ = flask.session
        request_ = flask.Request({
        })
        statement_ = args['statement']

        tag_selector = ('api-mnaccounts', )

        rv = policy_validation(
            session_,
            user_,
            request_,
            _re_spaces.sub(' ', statement_),
            tag_selector,
        )

        for level, idx, (tag, pred, action), res in rv:
            if isinstance(res, Exception):
                abort(400, msg='error in policy: {}'.format(res))

        return args


class UserTargetPolicyResource(SimpleResource):
    _model = UserTargetPolicy


class UserTargetResource(SimpleResource):
    _model = UserTarget


class TicketResource(SimpleResource):
    _model = Ticket
