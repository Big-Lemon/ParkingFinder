from schematics.types import (
    StringType,
    FloatType,
    IntType,
    DateTimeType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity

class Location(Entity):
    longitude = FloatType(required=True)
    latitude = FloatType(required=True)

    location = StringType(max_length=255, required=False)


class RealTimeLocation(Entity):
    """
    Parking Space Entity

    """
    # required variables
    token = StringType(min_length=1, max_length=7, required=True)
    vehicle_location = ModelType(model_class=Location)
    user_id = StringType(min_length=1, max_length=64, required=True)
    user_location = ModelType(model_class=Location)

    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')

    # non-required variables
    level = IntType(required=False)
    description = StringType(min_length=1, max_length=500, required=False)
