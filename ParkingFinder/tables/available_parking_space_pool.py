from ParkingFinder.tables.base import Base

import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    Enum,
)

class AvailableParkingSpacePool(Base):
    __tablename__ = 'available_parking_space_pool'

    plate = Column(String(7), ForeignKey('vehicles.plate'), primary_key=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(String(255), nullable=True)
    level = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return 'plate: {}, ' \
               'latitude: {}, ' \
               'longitude: {}, ' \
               'location: {}, ' \
               'level: {}, ' \
               'is_active: {}, ' \
               'created_at: {}' \
               'updated_at: {}'.format(
                self.plate,
                self.latitude,
                self.longitude,
                self.location,
                self.level,
                self.is_active,
                self.created_at,
                self.updated_at,
        )
