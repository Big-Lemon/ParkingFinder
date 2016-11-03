from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)

from ParkingFinder.tables.base import Base


class CheckOutParkingSpace(Base):
    __tablename__ = 'check_out_parking_space'

    user_id = Column(String(64), ForeignKey('users.user_id'), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    level = Column(Integer, nullable=True)
    description = Column(String(500), nullable=True)

    def __repr__(self):
        return 'user_id: {}, ' \
               'latitude: {}, ' \
               'longitude: {}, ' \
               'created_at: {}, ' \
               'level: {}, ' \
               'description: {}'.format(
                self.user_id,
                self.latitude,
                self.longitude,
                self.created_at,
                self.level,
                self.description,
        )
