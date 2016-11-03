from schematics.types import (
    DateTimeType,
    FloatType,
    StringType,
)

from ParkingFinder.entities.entity import Entity


class RealTime(Entity):
    """
    RealTime Entity
    """
    # required variables
    waiting_user_id  = StringType(min_length=1, max_length=64, required=True)
    waiting_user_latitude = FloatType(required=True)
    waiting_user_longitude = FloatType(required=True)
    request_user_id = StringType(min_length=1, max_length=64, required=True)
    request_user_latitude = FloatType(required=True)
    request_user_longitude = FloatType(required=True)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S')

