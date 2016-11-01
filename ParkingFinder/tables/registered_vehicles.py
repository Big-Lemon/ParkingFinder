from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    PrimaryKeyConstraint,
)

from ParkingFinder.tables.base import Base


class RegisteredVehicles(Base):
    __tablename__ = 'registered_vehicles'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'plate'), )

    user_id = Column(String(64), ForeignKey('users.user_id'), nullable=False)
    plate = Column(String(7), ForeignKey('vehicles.plate'), nullable=False)
    
    def __repr__(self):
        return 'user_id: {}, ' \
               'plate: {}, '.format(
                self.user_id,
                self.plate,
        )
