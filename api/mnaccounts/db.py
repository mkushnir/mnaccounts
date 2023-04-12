"""MN Accounts Service Database."""
import os
from datetime import date, datetime
import json
from argparse import ArgumentParser
import re

from sqlalchemy import engine_from_config, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .config import Config
from .model import Base, to_dict
from .utils import MyJSONEncoder

from .model.user import User
from .model.target import Target
from .model.policy import Policy
from .model.user_target_policy import UserTargetPolicy
from .model.ticket import Ticket
from .model.dbaudit import DbAudit

engine = None
session = None


@event.listens_for(Engine, 'connect')
def _prepare_sqlite(dbapi_connection, connection_record):
    c = dbapi_connection.cursor()
    c.execute('PRAGMA foreign_keys=ON')
    c.close()


def init():
    global engine, session
    engine = engine_from_config(Config()['DATABASE'])
    session = sessionmaker(engine, expire_on_commit=False)


_statment_parser = ArgumentParser()

_statment_parser.add_argument('-f', '--file')
_statment_parser.add_argument(
    '-n', '--normalize', default='0', action='store_true')

_re_spaces = re.compile(r'\s+')


def _maybe_load_statement(policy):
    st = policy['statement']

    if st.startswith('@'):
        args = _statment_parser.parse_args(
                _re_spaces.sub(' ', st[1:]).strip().split())

        if os.path.exists(args.file):
            with open(args.file) as f:
                s = f.read()

                if args.normalize:
                    s = _re_spaces.sub(' ', s)
                policy['statement'] = s
    return policy


def _insert_data(sess, fname):
    from .account import bcrypt

    with open(fname) as f:
        data = json.load(f)

        for i in data['user']:
            if 'password' in i:
                i['hash'] = bcrypt.generate_password_hash(i.pop('password'))
            sess.add(User(**i))

        for i in data['target']:
            sess.add(Target(**i))

        for i in data['policy']:
            if 'ts' in i:
                i['ts'] = datetime.strptime(i['ts'], '%Y-%m-%dT%H:%M:%S')
            sess.add(Policy(**_maybe_load_statement(i)))

        for i in data['user_target_policy']:
            sess.add(UserTargetPolicy(**i))

        for i in data['ticket']:
            if 'valid_since' in i:
                i['valid_since'] = datetime.strptime(i['valid_since'], '%Y-%m-%dT%H:%M:%S')
            if 'valid_until' in i:
                i['valid_until'] = datetime.strptime(i['valid_until'], '%Y-%m-%dT%H:%M:%S')
            sess.add(Ticket(**i))

        for i in data['dbaudit']:
            if 'dbts' in i:
                i['dbts'] = datetime.strptime(i['dbts'], '%Y-%m-%dT%H:%M:%S')
            sess.add(DbAudit(**i))

def _upsert_data(sess, fname, clear_utp=False):
    from .account import bcrypt

    with open(fname) as f:
        data = json.load(f)

        for i in data['user']:
            if 'password' in i:
                i['hash'] = bcrypt.generate_password_hash(i.pop('password'))

            user = sess.query(User).filter(User.id == i['id']).scalar()
            if user is None:
                sess.add(User(**i))
            else:
                for k, v in i.items():
                    setattr(user, k, v)

        for i in data['target']:
            target = sess.query(Target).filter(Target.id == i['id']).scalar()
            if target is None:
                sess.add(Target(**i))
            else:
                for k, v in i.items():
                    setattr(target, k, v)

        for i in data['policy']:
            policy = sess.query(Policy).filter(Policy.id == i['id']).scalar()
            i = _maybe_load_statement(i)

            if policy is None:
                sess.add(Policy(**i))

            else:
                for k, v in i.items():
                    setattr(policy, k, v)

        if clear_utp:
            sess.query(UserTargetPolicy).delete()

            for i in data['user_target_policy']:
                sess.add(UserTargetPolicy(**i))

def snapshot_data(sess, fname):
    res = {
        'user': [],
        'target': [],
        'policy': [],
        'user_target_policy': [],
        'ticket': [],
        'dbaudit': [],
    }

    users = sess.query(User)
    for i in users:
        res['user'].append(to_dict(i))

    targets = sess.query(Target)
    for i in targets:
        res['target'].append(to_dict(i))

    policies = sess.query(Policy)
    for i in policies:
        res['policy'].append(to_dict(i))

    utp = sess.query(UserTargetPolicy)
    for i in utp:
        res['user_target_policy'].append(to_dict(i))

    tickets = sess.query(Ticket)
    for i in tickets:
        res['ticket'].append(to_dict(i))

    dbaudit = sess.query(DbAudit)
    for i in dbaudit:
        res['dbaudit'].append(to_dict(i))

    with open(fname, 'w') as f:
        json.dump(res, f, cls=MyJSONEncoder, indent=2)



def reset():
    # init...
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    c = Config()
    if 'VOCABULARY_FILES' in c:
        with session() as sess:
            sess.execute(text('PRAGMA foreign_keys=OFF'))
            try:
                for fname in c['VOCABULARY_FILES']:
                    _insert_data(sess, fname)
                sess.commit()
            finally:
                sess.execute(text('PRAGMA foreign_keys=ON'))


def refresh(upsert_params=None):
    if upsert_params is None:
        upsert_params = {}
    c = Config()
    if 'VOCABULARY_FILES' in c:
        with session() as sess:
            for fname in c['VOCABULARY_FILES']:
                _upsert_data(sess, fname, **upsert_params)
            sess.commit()

def bootstrap():
    pass

def upgrade():
    pass
