from sqlalchemy import (
    Column,
    String,
)

from ParkingFinder.tables.base import Base


class Vehicle(Base):
    __tablename__ = 'vehicle'

    plate = Column(String(7), primary_key=True, index=True)
    color = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year  = Column(String(4), nullable=False)
    
    def __repr__(self):
        return 'plate: {}, ' \
               'color: {}, ' \
               'model: {}, ' \
               'year: {}'.format(
                self.plate,
                self.color,
                self.model,
                self.year,
        )