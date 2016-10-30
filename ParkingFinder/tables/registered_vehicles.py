from sqlalchemy import (
    Column,
    String,
)

from ParkingFinder.tables.base import Base


class RegisteredVehicles(Base):
    __tablename__ = 'registered_vehicles'

    user_id = Column(String(64), nullable=False)
    plate = Column(String(7), nullable=False)
    
    def __repr__(self):
        return 'user_id: {}, ' \
               'plate: {}, '.format(
                self.user_id,
                self.plate,
        )
