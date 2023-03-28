from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class DbAudit(Base):
    __tablename__ = 'dbaudit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dbts = Column(DateTime, index=True, nullable=False)
    dbuser = Column(String, index=True)
    dbmethod = Column(String, index=True, nullable=False)
    dbmodel = Column(String, index=True, nullable=False)
    dbdata = Column(String)
