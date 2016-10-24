from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
)

from ParkingFinder.tables.base import Base


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(String(64), primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    activated_vehicle = Column(String(7), nullable=True)
    profile_picture_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'user_id: {}, ' \
               'first_name: {}, ' \
               'last_name: {}, ' \
               'profile_picture_url: {}, ' \
               'activated_vehicle: {}, ' \
               'created_at: {}, ' \
               'updated_at: {}'.format(
                self.user_id,
                self.first_name,
                self.last_name,
                self.profile_picture_url,
                self.activated_vehicle,
                self.created_at,
                self.updated_at,
            )
