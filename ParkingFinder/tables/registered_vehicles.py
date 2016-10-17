from sqlalchemy import (
    Column,
    String,
)

from ParkingFinder.tables.base import Base

class Registered_vehicles(Base):
    __tablename__ = 'registered_vehicles'

    user_id = Column(String(64), ForeignKey('users.user_id'), index=True)
    plate = Column(String(7), nullable=False)
    
    def __repr__(self):
        return 'user_id: {}, ' \
               'plate: {}, '.format(
                self.user_id,
                self.plate,
        )
