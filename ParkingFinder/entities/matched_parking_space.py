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
    parking_space = ModelType(model_class=ParkingSpace)
    waiting_user = ModelType(model_class=WaitingUser)
    status = StringType(
        required=True,
        default='awaiting',
        choices=['awaiting', 'rejected', 'accepted'])
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
