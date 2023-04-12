from sqlalchemy import Column, BigInteger, Integer, Boolean, String, JSON, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class UserManage(Base):
    __tablename__ = 'usermanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation = Column(String, nullable=False, index=True)
    params = Column(JSON, nullable=True, index=False)
