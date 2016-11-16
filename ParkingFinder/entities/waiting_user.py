from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
    BooleanType,
)

from ParkingFinder.entities.entity import Entity


class WaitingUser(Entity):
    """
    Waiting User Entity

    """
    # required variables
    user_id = StringType(min_length=1, max_length=64, required=True)
    latitude = FloatType(required=True)
    longitude = FloatType(required=True)
    location = StringType(max_length=255, required=False)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
    is_active = BooleanType(required=True, default=False)

    # non-required variables
    level = IntType(required=False)
    description = StringType(min_length=1, max_length=500, required=False)

