from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class Policy(Base):
    __tablename__ = 'policy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False, index=True)
    statement = Column(String, nullable=False)

