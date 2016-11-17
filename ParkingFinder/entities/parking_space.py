from datetime import datetime
from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
)

from ParkingFinder.entities.entity import Entity


class ParkingSpace(Entity):
    """
    Parking Space Entity
    
    """
    # required variables
    plate = StringType(min_length=7, max_length=7, required=True)
    latitude = FloatType(required=True)
    longitude = FloatType(required=True)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f', default=datetime.utcnow)

    # non-required variables
    location = StringType(max_length=255, required=False)
    level = IntType(required=False)
