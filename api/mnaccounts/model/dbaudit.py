from sqlalchemy import Column, BigInteger, Integer, Boolean, String, JSON, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import mapped_column
# from sqlalchemy.ext.hybrid import hybrid_property
# from datetime import datetime

from . import Base

class DbAudit(Base):
    __tablename__ = 'dbaudit'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    dbts = mapped_column('dbts', DateTime, index=True, nullable=False)

    # @hybrid_property
    # def dbts(self):
    #     return self._dbts

    # @dbts.setter
    # def dbts(self, v):
    #     if isinstance(v, datetime):
    #         self._dbts = v
    #     else:
    #         self._dbts = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')

    dbuser = mapped_column(String, index=True)
    dbmethod = mapped_column(String, index=True, nullable=False)
    dbmodel = mapped_column(String, index=True, nullable=False)
    dbdata = mapped_column(JSON)
