from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class FlaskUser(Base):
    __tablename__ = 'flaskuser'

    id = Column(Integer, primary_key=True, autoincrement=True)

    login = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    hash = Column(String, nullable=True)
    apikey = Column(String, nullable=True, index=True)
    creds = Column(String, nullable=True)
    access_token = Column(String, nullable=True, index=True)
    id_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)

    is_authenticated = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_anonymous = Column(Boolean, nullable=False)

    policy = Column(String)
    authstate = Column(String, index=True)

    def get_id(self):
        return self.id

    def get_policy(self):
        return self.policy

UniqueConstraint(
    FlaskUser.login,
    name='uc_flaskuser_login',
)

UniqueConstraint(
    FlaskUser.hash,
    name='uc_flaskuser_hash',
)

UniqueConstraint(
    FlaskUser.apikey,
    name='uc_flaskuser_apikey',
)

UniqueConstraint(
    FlaskUser.access_token,
    name='uc_flaskuser_access_token',
)
