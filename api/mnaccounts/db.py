"""MN Accounts Service Database."""
from datetime import date, datetime
import json

from sqlalchemy import engine_from_config, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .config import Config
from .model import Base, to_dict

from .model.user import User
from .model.target import Target
from .model.policy import Policy
from .model.user_target_policy import UserTargetPolicy
from .model.ticket import Ticket

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


def _load_data(sess, fname):
    from .account import bcrypt
    with open(fname) as f:
        data = json.load(f)

        for i in data['user']:
            i['hash'] = bcrypt.generate_password_hash(i.pop('password'))
            sess.add(User(**i))

        for i in data['target']:
            sess.add(Target(**i))

        for i in data['policy']:
            sess.add(Policy(**i))

        for i in data['user_target_policy']:
            sess.add(UserTargetPolicy(**i))

def reset():
    # init...
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    c = Config()
    if 'VOCABULARY_FILES' in c:
        with session() as sess:
            for fname in c['VOCABULARY_FILES']:
                _load_data(sess, fname)
                sess.commit()


def bootstrap(catofile):
    pass

def upgrade(catofile):
    pass
