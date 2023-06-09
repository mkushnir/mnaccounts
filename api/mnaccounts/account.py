import json
import base64
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlencode, ParseResult, urlunparse

import flask
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt

import requests

import mnaccounts.db

from mnaccounts.utils import MyJSONEncoder

from mnaccounts.model import to_dict
from mnaccounts.model.user import User
from mnaccounts.model.target import Target
from mnaccounts.model.policy import Policy
from mnaccounts.model.user_target_policy import UserTargetPolicy
from mnaccounts.model.ticket import Ticket

from mnaccounts.model.flaskuser import FlaskUser

login_manager = LoginManager()
bcrypt = None
app = None


class ErrorTUTPRequest(ValueError):
    pass

def _tutp_from_request_args(session, request):
    for i in ('login', 'target', 'ticket'):
        if i not in request.args:
            raise ErrorTUTPRequest('missing arg {}'.format(i))

    res = session.query(
        Ticket, User, Target, Policy).filter(
            Ticket.user_id == User.id,
            Ticket.target_id == Target.id,
            Ticket.policy_id == Policy.id,
            User.login == request.args['login'],
            Target.label == request.args['target'],
            Ticket.ticket == request.args['ticket'],
        ).first()

    if res is None:
        raise ValueError('no such ticket: {}'.format(request.args['ticket']))

    return res

def _account_get():
    try:
        with mnaccounts.db.session() as session:
            try:
                ticket, user, target, policy = _tutp_from_request_args(session, flask.request)

                res = {
                    'ticket': to_dict(
                        ticket, except_=(
                            'id',
                            'user_id',
                            'target_id',
                            'policy_id',
                        )
                    ),
                    'user': to_dict(
                        user, except_=(
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
                    'target': to_dict(target, except_=('id',)),
                    'policy': to_dict(policy, except_=('id',)),
                }

            except ErrorTUTPRequest as e:
                if 'uinfo' not in flask.session:
                    raise ValueError('missing uinfo in session')

                res = flask.session['uinfo']

            rv = json.dumps(res, cls=MyJSONEncoder), 200

    except ValueError as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': ['_account_get', str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 401

    except Exception as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': ['_account_get', str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 400

    return rv


def validate_user_password(login, password):
    with mnaccounts.db.session() as session:
        user = session.query(User).filter(
            User.login == login,
            ).first()

        if user is not None:
            if bcrypt.check_password_hash(user.hash, password):
                user.creds = None
                user.access_token = None
                user.id_token = None
                user.refresh_token = None
                user.is_authenticated = True
                session.commit()

                return user
    return None


def validate_apikey(apikey):
    with mnaccounts.db.session() as session:
        user = session.query(User).filter(
            User.apikey == apikey,
            ).first()

    return user


def _account_post():
    u = None
    try:
        data = flask.request.json

        if 'login' in data and 'password' in data:
            u = data['login']
            user = validate_user_password(data['login'], data['password'])

        elif 'apikey' in data:
            u = data['apikey']
            user = validate_apikey(data['apikey'])

        else:
            user  = None

        if user is None:
            app.logger.debug('login failure data {}'.format(data))
            raise ValueError('wrong credentails for {}'.format(u))

        with mnaccounts.db.session() as session:
            res = session.query(Target, UserTargetPolicy).filter(
                UserTargetPolicy.target_id == Target.id,
                UserTargetPolicy.user_id == user.id,
                Target.label == data['target'],
            ).first()

            if res is None:
                app.logger.debug('login failure data {}'.format(data))
                raise ValueError('wrong target {} for {}'.format(
                    data['target'], u))

            target, utp = res

            ticket_ = secrets.token_urlsafe()

            since = datetime.utcnow()

            if user.ticket_lifetime is not None:
                lifetime = user.ticket_lifetime
            else:
                lifetime = app.config['TICKET_LIFETIME_SECONDS']

            until = since + timedelta(seconds=lifetime)

            ticket = Ticket(
                user_id=user.id,
                target_id=target.id,
                policy_id=utp.policy_id,
                valid_since=since,
                valid_until=until,
                ticket=ticket_,
            )

            session.add(ticket)
            session.commit()

            u0 = urlparse(target.url)
            q0 = parse_qs(u0.query)
            q0['login'] = user.login
            q0['target'] = target.label
            q0['ticket'] = ticket_

            if 'mode' in flask.request.args and flask.request.args['mode'] == 'short':
                res = q0
                rv = flask.make_response(json.dumps(res, cls=MyJSONEncoder))

            else:
                q1 = urlencode(q0, doseq=True)
                u1 = ParseResult(
                    u0.scheme, u0.netloc, u0.path, u0.params, q1, u0.fragment)

                gonext = urlunparse(u1)

                #app.logger.info('u0 {}'.format(u0))
                #app.logger.info('q0 {}'.format(q0))
                #app.logger.info('q1 {}'.format(q1))
                #app.logger.info('u1 {}'.format(u1))
                #app.logger.info('gonext {}'.format(gonext))

                rv = flask.redirect(gonext, code=302)

    except ValueError as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': [u, str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 401

    except Exception as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': [u, str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 400

    return rv


def _account_delete():
    try:
        data = flask.request.json

        with mnaccounts.db.session() as session:
            ndeleted = session.query(Ticket).filter(
                Ticket.ticket == data['ticket']).delete()
            session.commit()

        res = {
            'data': {
                'ndeleted': ndeleted,
            }
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 200

    except Exception as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': [data['ticket'], str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 400

    return rv



#
# api client
#
@login_manager.request_loader
def load_user_from_request(request):
    #app.logger.info('SESS {}'.format(flask.session))

    if 'uinfo' not in flask.session:
        return None

    else:
        uinfo = flask.session['uinfo']

    user = validate_mnaccount(uinfo)

    return user


def validate_mnaccount(uinfo):
    ticket = uinfo['ticket']
    since = datetime.strptime(ticket['valid_since'], '%Y-%m-%dT%H:%M:%S')
    until = datetime.strptime(ticket['valid_until'], '%Y-%m-%dT%H:%M:%S')
    now = datetime.utcnow()
    user = None

    if (now < since) or (now > until):
        app.logger.warning('expired uinfo{} now {}'.format(uinfo, now))
    else:
        user = FlaskUser(**uinfo['user'])
        user.policy = uinfo['policy']['statement']

    return user


def login_mnaccount():
    try:
        headers = {
            'Accept': 'application/json',
        }

        params = {
            'login': flask.request.args['login'],
            'target': flask.request.args['target'],  # it's me
            'ticket': flask.request.args['ticket'],
        }

        if 'MNACCOUNTS_AUTH_PARAMS' in app.config:
            params.update(app.config['MNACCOUNTS_AUTH_PARAMS'])

        mnaccount_url = app.config['MNACCOUNTS_AUTH_URI']
        response = requests.get(
            mnaccount_url,
            headers=headers,
            params=params,
        )

        if response.status_code != 200:
            raise Exception(['mnaccount', response.text])

        else:
            uinfo = response.json()

            user = validate_mnaccount(uinfo)

            if user is None:
                app.logger.debug('login failure params {}'.format(params))
                raise ValueError('wrong credentails for ticket {}'.format(params['ticket']))

            if not login_user(user):
                app.logger.debug('login failure user {}'.format(to_dict(user)))
                raise ValueError('wrong user props {} for ticket {}'.format(
                    to_dict(user, except_=(
                        'hash',
                        'apikey',
                        'creds',
                        'access_token',
                        'id_token',
                        'refresh_token',
                        'authstate',
                    )),
                    params['ticket'],
                ))

            flask.session['uinfo'] = uinfo

            #app.logger.info('mnaccount {}'.format(uinfo))

            res = {
                'data': uinfo
            }

            rv = flask.make_response(json.dumps(res, cls=MyJSONEncoder))

            return rv

    except ValueError as e:
        app.logger.exception('login_mnaccount exception')
        res = {
            'msg': 'mnLoginFailure',
            'args': ['ticket', str(e)],
        }
        return json.dumps(res, cls=MyJSONEncoder), 401

    except Exception as e:
        app.logger.exception('login_mnaccount exception')
        res = {
            'msg': 'mnLoginFailure',
            'args': ['ticket', str(e)],
        }
        return json.dumps(res, cls=MyJSONEncoder), 400

#def _qwe(*args, **kwargs):
#    app.logger.info('qwe {}'.format(flask.request.headers))


def init(app_):
    global bcrypt, app

    app = app_

    login_manager.init_app(app)

    app.add_url_rule(
        '/account',
        view_func=_account_get,
        methods=['GET'])

    app.add_url_rule(
        '/account',
        view_func=_account_post,
        methods=['POST'])

    app.add_url_rule(
        '/account',
        view_func=_account_delete,
        methods=['DELETE'])

    app.add_url_rule(
        '/mnaccount',
        view_func=login_mnaccount,
        methods=['GET'])

    bcrypt = Bcrypt(app)

    #app.before_request(_qwe)
