from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False, index=True)
    url = Column(String, nullable=False, index=True)


UniqueConstraint(
    Target.label,
    name='uc_target_label',
)
