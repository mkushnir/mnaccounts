"""Simple db access."""
import re
import json

import flask
from flask_login import current_user
from flask_restful import abort

import black
import black.mode

from ..model.flaskuser import FlaskUser
from ..model.dbaudit import DbAudit

from ..model.user import User
from ..model.target import Target
from ..model.policy import Policy
from ..model.user_target_policy import UserTargetPolicy
from ..model.user_target import UserTarget
from ..model.ticket import Ticket

from . import SimpleResource

from mnaccounts.policy import policy_parse, policy_validation

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
    _black_mode = black.mode.Mode(
        # target_versions={black.TargetVersion.PY33},
        line_length=74,
        # magic_trailing_comma=False,
    )

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

    @classmethod
    def _format_statement(cls, s):
        res = []

        items = policy_parse(s)
        for tag, predicate, action in items:
            if tag.startswith('api-'):
                predicate = black.format_str(predicate, mode=cls._black_mode).strip()
            elif tag.startswith('gui-'):
                predicate = json.dumps(json.loads(predicate), indent=4)
            else:
                predicate = predicate.strip()

            action = action.strip() if action is not None else ''
            res.append('{}{}{}{};'.format(
                tag,
                # ' ' if predicate.startswith('policy.load') else '\n',
                ' ' if (not action) else '\n',
                predicate,
                '\n{}{}'.format(' ' * 72, action) if action else ''))

        return '\n'.join(res)

    def _pre_return(self, req, args, o):
        if req.method == 'GET':
            if type(o) == list:
                for i in o:
                    i['statement'] = self._format_statement(i['statement'])
        else:
            o['statement'] = self._format_statement(o['statement'])


class UserTargetPolicyResource(SimpleResource):
    _model = UserTargetPolicy


class UserTargetResource(SimpleResource):
    _model = UserTarget


class TicketResource(SimpleResource):
    _model = Ticket
