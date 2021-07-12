from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    BigInteger, Boolean, DateTime, String,
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    telegram_info = Column(String())
    name = Column(String(32), nullable=False)

    reservations = relationship('Reservation', back_populates='user')


class Event(Base):
    __tablename__ = 'event'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(128), nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    sections = relationship('Section', back_populates='event')


class Section(Base):
    __tablename__ = 'section'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(128), nullable=False)
    event_id = Column(
        BigInteger,
        ForeignKey('event.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    event = relationship('Event', back_populates='sections')
    reservations = relationship('Reservation', back_populates='section')


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(128), nullable=False)
    section_id = Column(
        BigInteger,
        ForeignKey('section.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    user_id = Column(
        BigInteger,
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True
    )
    updated = Column(DateTime, nullable=True)

    section = relationship('Section', back_populates='reservations')
    user = relationship('User', back_populates='reservations')
