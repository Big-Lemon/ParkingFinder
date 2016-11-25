import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)

from ParkingFinder.tables.base import Base


class ParkingLot(Base):
    __tablename__ = 'parking_lot'

    plate = Column(String(7), ForeignKey('vehicles.plate'), primary_key=True)
    latitude = Column(String(16), nullable=False)
    longitude = Column(String(16), nullable=False)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    level = Column(Integer, nullable=True)

    def __repr__(self):
        return 'plate: {}, ' \
            'latitude: {}, ' \
            'longitude: {}, ' \
            'location: {}, '\
            'created_at: {}, '\
            'level: {}, '.format(
                self.plate,
                self.latitude,
                self.longitude,
                self.location,
                self.created_at,
                self.level,
        )
