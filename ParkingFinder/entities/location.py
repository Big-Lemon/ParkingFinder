from schematics.types import (
    StringType,
    FloatType,
    IntType
)

from ParkingFinder.entities.entity import Entity


class Location(Entity):
    """
    Location Entity
    """
    # required variables
    longitude = FloatType(required=True)
    latitude = FloatType(required=True)

    # non-required variables
    location = StringType(min_length=1, max_length=255, required=False)
    level = IntType(required=False)