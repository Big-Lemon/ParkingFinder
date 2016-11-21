from datetime import datetime, timedelta

from clay import config
from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
)

from ParkingFinder.entities.entity import Entity


class MatchedParkingSpace(Entity):
    """
    Parking Space Entity

    """
    # required variables
    plate = StringType(min_length=1, max_length=7, required=True)
    user_id = StringType(min_length=1, max_length=64, required=True)
    status = StringType(
        required=True,
        default='awaiting',
        choices=['awaiting', 'rejected', 'reserved', 'expired'])
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f', default=datetime.utcnow)

    @property
    def is_reserved(self):
        return self.status == 'reserved'

    @property
    def is_awaiting(self):
        return self.status == 'awaiting'

    @property
    def is_rejected(self):
        return self.status == 'rejected'

    @property
    def is_expired(self):

        if self.status == 'expired':
            return True
        else:
            current = datetime.utcnow()
            delta = config.get('posted_parking.timeout')
            return self.created_at + timedelta(0, delta) < current

    @property
    def is_time_expired(self):
        current = datetime.utcnow()
        delta = config.get('posted_parking.timeout')
        return self.created_at + timedelta(0, delta) < current

