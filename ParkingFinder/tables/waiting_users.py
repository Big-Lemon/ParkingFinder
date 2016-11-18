import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
)

from ParkingFinder.tables.base import Base

class WaitingUsers(Base):
    __tablename__ = 'waiting_pool'

    user_id = Column(String(64), ForeignKey('users.user_id'), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(String(255), nullable=True)
    level = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


    def __repr__(self):
        return 'user_id: {}, ' \
               'latitude: {}, ' \
               'longitude: {}, ' \
               'location: {}, ' \
               'level: {}, '\
               'is_active: {} '\
               'created_at: {}, ' .format(
                self.user_id,
                self.latitude,
                self.longitude,
                self.location,
                self.level,
                self.is_active,
                self.created_at,
            )
