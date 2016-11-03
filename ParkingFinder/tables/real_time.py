import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from ParkingFinder.tables.base import Base


class RealTimes(Base):
    __tablename__ = 'real_time'

    waiting_user_id = Column(String(64), ForeignKey('users.user_id'), primary_key=True)
    waiting_user_latitude = Column(Float, nullable=False)
    waiting_user_longitude = Column(Float, nullable=False)
    request_user_id = Column(String(64), ForeignKey('users.user_id'))
    request_user_latitude = Column(Float, nullable=False)
    request_user_longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return 'waiting_user_id: {}, ' \
               'waiting_user_latitude: {}, ' \
               'waiting_user_longitude: {}, ' \
               'request_user_id: {}, ' \
               'request_user_latitude: {}, ' \
               'request_user_longitude: {}, ' \
               'created_at: {} '.format(
                self.waiting_user_id,
                self.waiting_user_latitude,
                self.waiting_user_longitude,
                self.request_user_id,
                self.request_user_latitude,
                self.request_user_longitude,
                self.created_at,
        )
