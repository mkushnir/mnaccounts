from sqlalchemy import Column, BigInteger, Integer, Boolean, String, Date, DateTime, ForeignKey, Index, UniqueConstraint, select

from . import Base
from ..utils import view


from .user_target_policy import UserTargetPolicy
from .target import Target


class UserTarget(Base):
    __table__ = view(
        'user_target',
        select(
            UserTargetPolicy.id,
            UserTargetPolicy.user_id,
            Target.label,
            Target.url,
        ).filter(
            UserTargetPolicy.target_id == Target.id,
        ),
        metadata=Base.metadata,
    )

    __tablename__ = 'user_target'

