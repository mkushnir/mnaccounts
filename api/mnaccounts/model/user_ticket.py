from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index

from . import Base

class UserTicket(Base):
    __tablename__ = 'user_ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=False, ForeignKey('user.id'))
    ticket = Column(String, index=True, nullable=False)


UniqueConstraint(
    UserTicket.user_id,
    UserTicket.ticket,
    name='ix_user_ticket_user_id_ticket',
)
