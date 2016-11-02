import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from ParkingFinder.tables.base import Base


class UserReserved(Base):
    __tablename__ = 'user_reserved'

    user_id = Column(String(64), ForeignKey('users.user_id'), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return 'user_id: {}, ' \
               'latitude: {}, ' \
               'longitude: {}, ' \
               'created_at: {} '.format(
                self.space_id,
                self.latitude,
                self.longitude,
                self.created_at,
        )
