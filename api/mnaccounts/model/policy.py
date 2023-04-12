from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index, func
from sqlalchemy.orm import mapped_column
# from sqlalchemy.ext.hybrid import hybrid_property
# from datetime import datetime

from . import Base
from ..utils import trigger

class Policy(Base):
    __tablename__ = 'policy'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    label = mapped_column(String, nullable=False, index=True)
    statement = mapped_column(String, nullable=False)
    ts = mapped_column('ts', DateTime, index=True, nullable=False, default=func.DATETIME())

    # @hybrid_property
    # def ts(self):
    #     return self._ts

    # @ts.setter
    # def ts(self, v):
    #     if isinstance(v, datetime):
    #         self._ts = v
    #     else:
    #         self._ts = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')

trigger('tr_policy_ts', 'before update', 'policy', None, 'update policy set ts = datetime() where id = OLD.id', Policy.metadata)
