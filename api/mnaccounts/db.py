"""MN Accounts Service Database."""
import logging
from datetime import date, datetime
import csv

from sqlalchemy import engine_from_config, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .logger import get_logger
from .config import Config
from .model import Base, to_dict

from .model.user import User

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


def _load_users(sess):
    from .login import bcrypt

    sess.add_all([
        User(
            id=1,
            login='mkushnir',
            email='markiyan.kushnir@gmail.com',
            hash=bcrypt.generate_password_hash('123456'),
            apikey='123456',
            is_authenticated=True,
            is_active=True,
            is_anonymous=False,
        ),
        User(
            id=2,
            login='alice',
            email='vfhrszyreiysh@gmail.com',
            hash=bcrypt.generate_password_hash('123456'),
            apikey='234567',
            is_authenticated=True,
            is_active=True,
            is_anonymous=False,
        ),
    ])


def _load_vocabs(sess):
    pass


def reset():
    # init...
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with session() as sess:
        _load_users(sess)
        _load_vocabs(sess)
        sess.commit()


def bootstrap(catofile):
    pass

def upgrade(catofile):
    pass
