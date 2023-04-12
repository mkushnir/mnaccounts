"""Manage Resource."""
import io
import json
import re
from datetime import datetime

import flask
from flask.sessions import SecureCookieSessionInterface
from flask_restful import abort
from flask_login import current_user

from ..utils import MyJSONEncoder

from .. import db

from ..model import to_dict

from ..model.dbaudit import DbAudit
from ..model.user import User
from ..model.target import Target
from ..model.policy import Policy
from ..model.user_target_policy import UserTargetPolicy
from ..model.ticket import Ticket
from ..model.usermanage import UserManage
from ..model.policymanage import PolicyManage

from mnaccounts.resource import SimpleResource
from mnaccounts.policy import policy_validation

class UserManageResource(SimpleResource):
    _model = UserManage

    def get(self, id=None):
        raise NotImplementedError()

    def post(self, id=None):
        raise NotImplementedError()

    def put(self, id=None):
        args = self._model_parser.parse_args(flask.request)
        args = self._prepare_args(flask.request, args)

        with db.session() as session:
            user = session.query(User).filter(User.id == id).scalar()

            if user is None:
                abort(400, msg='invalid user_id: {}'.format(id))

            o = self._model(**args)

            if o.operation == 'set-active':
                flag = o.params['flag']

                if flag:
                    if not user.is_active:
                        user.is_active = True
                else:
                    if user.is_active:
                        user.is_active = False

                        tickets = session.query(Ticket).filter(
                                Ticket.user_id == id)

                        for i in tickets:
                            session.delete(i)

            elif o.operation == 'set-target-policy':
                target_ = o.params['target']
                policy_ = o.params['policy']

                target = session.query(Target).filter(
                    Target.label == target_).scalar()

                if target is None:
                    abort(400, msg='invalid target: {}'.format(target_))

                utp = session.query(UserTargetPolicy).filter(
                    UserTargetPolicy.user_id == user.id,
                    UserTargetPolicy.target_id == target.id).scalar()

                if utp is None:
                    if policy_ is None:
                        abort(
                            400, msg='no utp for target: {}'.format(target_))
                    else:
                        policy = session.query(Policy).filter(
                            Policy.label == policy_).scalar()

                        if policy is None:
                            abort(
                                400,
                                msg='invalid policy: {}'.format(policy_))

                        utp = UserTargetPolicy(
                            user_id=user.id,
                            target_id=target.id,
                            policy_id=policy.id
                        )
                        session.add(utp)
                else:
                    if policy_ is None:
                        session.delete(utp)
                    else:
                        policy = session.query(Policy).filter(
                            Policy.label == policy_).scalar()

                        if policy is None:
                            abort(
                                400,
                                msg='invalid policy: {}'.format(policy_))

                        if utp.policy_id != policy.id:
                            utp.policy_id = policy.id

            else:
                abort(400, msg='invalid operation: {}'.format(o.operation))

            data = to_dict(o)

            audit = DbAudit(
                id=None,
                dbts=datetime.utcnow(),
                dbuser=current_user.login,
                dbmethod='update',
                dbmodel=self._model.__table__.name,
                dbdata=data,
            )
            session.add(audit)

            session.commit()

        self._post_commit(flask.request, args, o)

        return {
            'data': data
        }

    def delete(self, id=None):
        raise NotImplementedError()


_re_spaces = re.compile(r'\s+')

class PolicyManageResource(SimpleResource):
    _model = PolicyManage

    def get(self, id=None):
        raise NotImplementedError()

    def post(self, id=None):
        raise NotImplementedError()

    @staticmethod
    def _cleanup_args(o):
        if 'wsgi.input' in o.params['request']:
            o.params['request']['wsgi.input'].seek(0)
            o.params['request']['wsgi.input'] = \
                    o.params['request']['wsgi.input'].read().decode('utf-8')

        if 'werkzeug.request' in o.params['request']:
            o.params['request'].pop('werkzeug.request')

        return o

    def put(self, id=None):
        args = self._model_parser.parse_args(flask.request)
        args = self._prepare_args(flask.request, args)

        with db.session() as session:
            o = self._model(**args)

            policy = session.query(Policy).filter(Policy.id == id).scalar()

            if policy is None:
                if 'statement' in o.params:
                    statement_ = o.params['statement']
                else:
                    abort(
                        400,
                        msg='invalid policy_id: {} and no statement '
                        'in params'.format(id))
            else:
                statement_ = policy.statement

            if o.operation == 'validate':
                if 'request' in o.params:
                    if 'wsgi.input' in o.params['request']:
                        o.params['request']['wsgi.input'] = io.BytesIO(
                            o.params['request']['wsgi.input'].encode('utf-8'))

                    request_ = flask.Request(o.params['request'])

                else:
                    request_ = flask.request

                if 'login' in o.params and 'target' in o.params:
                    res = session.query(
                        User, Target, Policy, UserTargetPolicy
                    ).filter(
                        User.id == UserTargetPolicy.user_id,
                        Target.id == UserTargetPolicy.target_id,
                        Policy.id == UserTargetPolicy.policy_id,
                        User.login == o.params['login'],
                        Target.label == o.params['target'],
                    ).first()

                    if res is None:
                        user_ = current_user
                        session_ = flask.session
                    else:
                        user_, target_, policy_, utp_ = res
                        uinfo = {
                            'ticket': {'ticket': 'fake'},
                            'user': to_dict(
                                user_, except_=(
                                    # 'id',
                                    'hash',
                                    # 'apikey',
                                    'creds',
                                    'access_token',
                                    'id_token',
                                    'refresh_token',
                                    'authstate',
                                )
                            ),
                            'target': to_dict(target_, except_=('id',)),
                            'policy': to_dict(policy_, except_=('id',)),
                        }

                        session_ = SecureCookieSessionInterface.session_class(
                            {
                                '_id': 'fake',
                                '_user_id': str(user_.id),
                                'uinfo': uinfo,
                            }
                        )
                else:
                    user_ = current_user
                    session_ = flask.session

                tag_selector = o.params.get('tag-selector')

                try:
                    rv = policy_validation(
                        session_,
                        user_,
                        request_,
                        _re_spaces.sub(' ', statement_),
                        tag_selector,
                    )

                except Exception as e:
                    from mnaccounts.app import app
                    app.logger.exception('error in operation:')

                    data = to_dict(self._cleanup_args(o))

                    abort(400, msg='error in operation: {}'.format(
                        json.dumps(data, cls=MyJSONEncoder)))

            else:
                data = to_dict(self._cleanup_args(o))
                abort(400, msg='invalid operation: {}'.format(data))

            data = to_dict(self._cleanup_args(o))

            audit = DbAudit(
                id=None,
                dbts=datetime.utcnow(),
                dbuser=current_user.login,
                dbmethod='update',
                dbmodel=self._model.__table__.name,
                dbdata=data,
            )
            session.add(audit)

            session.commit()

        self._post_commit(flask.request, args, o)

        return {
            'data': rv
        }

    def delete(self, id=None):
        raise NotImplementedError()
