from datetime import datetime

from schematics.types import (
    BooleanType,
    DateTimeType,
    FloatType,
    StringType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.parking_space import ParkingSpace


class AvailableParkingSpace(Entity):
    """
    Parking Space Entity with posting status

    """
    # required variables

    plate = StringType(min_length=1, max_length=7, required=True)
    latitude = FloatType(required=True)
    longitude = FloatType(required=True)
    location = StringType(max_length=255, required=False)
    is_active = BooleanType(required=True, default=False)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f', default=datetime.utcnow)
    updated_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f', default=datetime.utcnow)
