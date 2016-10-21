from sqlalchemy import (
    Column,
    String,
    Integer,
)

from ParkingFinder.tables.base import Base


class Vehicles(Base):
    __tablename__ = 'vehicles'

    plate = Column(String(7), primary_key=True)
    brand = Column(String(32), nullable=False)
    model = Column(String(32), nullable=False)
    color = Column(String(32), nullable=False)
    year  = Column(Integer, nullable=False)

    def __repr__(self):
        return 'plate: {}, ' \
               'brand: {}, ' \
               'model: {}, ' \
               'color: {}, ' \
               'year: {}'.format(
                self.plate,
                self.brand,
                self.model,
                self.color,
                self.year,
        )
