from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import mapped_column
# from sqlalchemy.ext.hybrid import hybrid_property
# from datetime import datetime

from . import Base

class Ticket(Base):
    __tablename__ = 'ticket'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    target_id = mapped_column(Integer, ForeignKey('target.id', ondelete='CASCADE'), index=True, nullable=False)
    policy_id = mapped_column(Integer, ForeignKey('policy.id', ondelete='CASCADE'), index=True, nullable=False)
    valid_since = mapped_column('valid_since', DateTime, index=True, nullable=False)

    # @hybrid_property
    # def valid_since(self):
    #     return self._valid_since

    # @valid_since.setter
    # def valid_since(self, v):
    #     if isinstance(v, datetime):
    #         self._valid_since = v
    #     else:
    #         self._valid_since = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')

    valid_until = mapped_column('valid_until', DateTime, index=True, nullable=True)

    # @property
    # def valid_until(self):
    #     return self._valid_until

    # @valid_until.setter
    # def valid_until(self, v):
    #     if isinstance(v, datetime):
    #         self._valid_until = v
    #     else:
    #         self._valid_until = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')

    ticket = mapped_column(String, index=True, nullable=False)

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
