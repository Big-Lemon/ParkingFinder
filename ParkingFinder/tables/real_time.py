import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)

from ParkingFinder.tables.base import Base


class RealTime(Base):
    __tablename__ = 'real_time'
    __table_args__ = (PrimaryKeyConstraint('user_one_id', 'user_two_id'), )

    user_one_id = Column(String(64), ForeignKey('users.user_id'))
    user_two_id = Column(String(64), ForeignKey('users.user_id'))
    latitude_one = Column(Float, nullable=False)
    longitude_one = Column(Float, nullable=False)
    latitude_two = Column(Float, nullable=False)
    longitude_two = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return 'user_one_id: {}, ' \
               'latitude_one: {}, ' \
               'longitude_one: {}, ' \
               'user_two_id: {}, ' \
               'latitude_two: {}, ' \
               'longitude_two: {}, ' \
               'created_at: {} '.format(
                self.user_one_id,
                self.latitude_one,
                self.longitude_one,
                self.user_two_id,
                self.latitude_two,
                self.longitude_two,
                self.created_at,
        )
