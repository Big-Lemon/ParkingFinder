from datetime import datetime

from clay import config
from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.parking_space import ParkingSpace
from ParkingFinder.entities.waiting_user import WaitingUser


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
        choices=['awaiting', 'rejected', 'accepted', 'expired'])
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')

    @property
    def is_accepted(self):
        return self.status == 'accepted'

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
            return self.created_at + config.get('matching.awaiting_action_timeout') < current
