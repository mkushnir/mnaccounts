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


def _account_get():
    try:
        with mnaccounts.db.session() as session:
            res = session.query(
                Ticket, User, Target, Policy).filter(
                    Ticket.user_id == User.id,
                    Ticket.target_id == Target.id,
                    Ticket.policy_id == Policy.id,
                    User.login == flask.request.args['login'],
                    Target.label == flask.request.args['target'],
                    Ticket.ticket == flask.request.args['ticket'],
                ).first()

            if res is None:
                raise ValueError('no such ticket: {}'.format(ticket))

            ticket, user, target, policy = res

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
                        #'id',
                        'hash',
                        'apikey',
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


def validate_credentials(login, password):
    #app.logger.info('validate_credentials {} {}'.format(login, password))

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



def _account_post():
    try:
        data = flask.request.json

        user = validate_credentials(data['login'], data['password'])

        if user is None:
            app.logger.debug('login failure data {}'.format(data))
            raise ValueError('wrong credentails for {}'.format(data['login']))

        with mnaccounts.db.session() as session:
            res = session.query(Target, UserTargetPolicy).filter(
                UserTargetPolicy.target_id == Target.id,
                UserTargetPolicy.user_id == user.id,
                Target.label == data['target'],
            ).first()

            if res is None:
                app.logger.debug('login failure data {}'.format(data))
                raise ValueError('wrong target {} for {}'.format(
                    data['target'], data['login']))

            target, utp = res

            ticket_ = secrets.token_urlsafe()

            since = datetime.utcnow()
            until = since + timedelta(seconds=app.config['TICKET_LIFETIME_SECONDS'])

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
            'args': [data['login'], str(e)],
        }
        rv = json.dumps(res, cls=MyJSONEncoder), 401

    except Exception as e:
        app.logger.exception('account exception')
        res = {
            'msg': 'mnAccountFailure',
            'args': [data['login'], str(e)],
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

    if 'creds' not in flask.session:
        return None

    user = validate_mnaccount(flask.session['creds'])

    return user


def validate_mnaccount(creds):
    ticket = creds['ticket']
    since = datetime.strptime(ticket['valid_since'], '%Y-%m-%dT%H:%M:%S')
    until = datetime.strptime(ticket['valid_until'], '%Y-%m-%dT%H:%M:%S')
    now = datetime.utcnow()
    user = None

    if (now < since) or (now > until):
        app.logger.warning('expired creds{} now {}'.format(creds, now))
    else:
        user = FlaskUser(**creds['user'])
        user.policy = creds['policy']['statement']

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

        if 'MNACCOUNT_AUTH_PARAMS' in app.config:
            params.update(app.config['MNACCOUNT_AUTH_PARAMS'])

        mnaccount_url = app.config['MNACCOUNT_AUTH_URI']
        response = requests.get(
            mnaccount_url,
            headers=headers,
            params=params,
        )

        if response.status_code != 200:
            raise Exception(['mnaccount', response.text])

        else:
            creds = response.json()

            user = validate_mnaccount(creds)

            if user is None:
                app.logger.debug('login failure params {}'.format(params))
                raise ValueError('wrong credentails for ticket {}'.format(params['ticket']))

            login_user(user)

            flask.session['creds'] = creds

            #app.logger.info('mnaccount {}'.format(creds))

            res = {
                'data': creds
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
