from ParkingFinder.tables.base import Base

import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
)

class MatchedParkingSpaceList(Base):
    __tablename__ = 'matched_parking_space_list'

    user_id = Column(String(64), ForeignKey('users.user_id'), nullable=False)
    plate = Column(String(7), ForeignKey('vehicles.plate'), primary_key=True, nullable=False)
    # status = Column(String(8), nullable=False, default='awaiting')
    status = Column(Enum('awaiting', 'rejected', 'reserved', 'expired', name='status_types'), nullable=False, default='awaiting')
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return 'user_id: {}, ' \
               'plate: {}, ' \
               'status: {}, '\
               'created_at: {}'.format(
                self.user_id,
                self.plate,
                self.status,
                self.created_at,
        )