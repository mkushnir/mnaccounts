from sqlalchemy import Column, BigInteger, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class UserTargetPolicy(Base):
    __tablename__ = 'user_target_policy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    target_id = Column(Integer, ForeignKey('target.id', ondelete='CASCADE'), nullable=False)
    policy_id = Column(Integer, ForeignKey('policy.id', ondelete='CASCADE'), nullable=False)

Index(
    'ix_user_target_policy_user_id_target_id',
    UserTargetPolicy.user_id,
    UserTargetPolicy.target_id,
)

UniqueConstraint(
    UserTargetPolicy.user_id,
    UserTargetPolicy.target_id,
    name='uc_user_target_policy_user_id_target_id',
)
