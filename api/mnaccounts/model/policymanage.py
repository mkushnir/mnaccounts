from sqlalchemy import Column, BigInteger, Integer, Boolean, String, JSON, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class PolicyManage(Base):
    __tablename__ = 'policymanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation = Column(String, nullable=False, index=True)
    params = Column(JSON, nullable=True, index=False)
