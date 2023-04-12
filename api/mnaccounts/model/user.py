from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)

    login = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    hash = Column(String, nullable=True)
    apikey = Column(String, nullable=True, index=True)
    creds = Column(String, nullable=True)
    access_token = Column(String, nullable=True, index=True)
    id_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)

    # flask
    is_authenticated = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_anonymous = Column(Boolean, nullable=False)

    authstate = Column(String, index=True)
    ticket_lifetime = Column(Integer, nullable=True)


UniqueConstraint(
    User.login,
    name='uc_user_login',
)


UniqueConstraint(
    User.hash,
    name='uc_user_hash',
)


UniqueConstraint(
    User.apikey,
    name='uc_user_apikey',
)


UniqueConstraint(
    User.access_token,
    name='uc_user_access_token',
)
