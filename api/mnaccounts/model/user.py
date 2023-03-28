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

    # 
    is_authenticated = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_anonymous = Column(Boolean, nullable=False)

    policy = Column(String)
    authstate = Column(String, index=True)

    # 
    def get_id(self):
        return self.id

    def get_policy(self):
        return self.policy


UniqueConstraint(
    User.login,
    name='ix_user_login',
)


UniqueConstraint(
    User.hash,
    name='ix_user_hash',
)


UniqueConstraint(
    User.apikey,
    name='ix_user_apikey',
)


UniqueConstraint(
    User.access_token,
    name='ix_user_access_token',
)
