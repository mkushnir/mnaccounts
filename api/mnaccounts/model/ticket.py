from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    target_id = Column(Integer, ForeignKey('target.id', ondelete='CASCADE'), index=True, nullable=False)
    policy_id = Column(Integer, ForeignKey('policy.id', ondelete='CASCADE'), index=True, nullable=False)
    valid_since = Column(DateTime, index=True, nullable=False)
    valid_until = Column(DateTime, index=True, nullable=True)
    ticket = Column(String, index=True, nullable=False)

UniqueConstraint(
    Ticket.ticket,
    name='uc_ticket_ticket',
)

#UniqueConstraint(
#    Ticket.user_id,
#    Ticket.target_id,
#    Ticket.policy_id,
#    name='uc_ticket_user_id_target_id_policy_id',
#)
