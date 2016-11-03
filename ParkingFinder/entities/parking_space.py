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
    user_id = StringType(min_length=1, max_length=64, required=True)
    latitude = FloatType(required=True)
    longitude = FloatType(required=True)
    created_at = DateTimeType(required=True)

    # non-required variables
    level = IntType(required=False)
    description = StringType(min_length=1, max_length=500, required=False)
