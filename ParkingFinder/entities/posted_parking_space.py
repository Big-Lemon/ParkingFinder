from schematics.types import (
    BooleanType,
    DateTimeType,
)
from schematics.types.compound import ModelType

from ParkingFinder.entities.entity import Entity
from ParkingFinder.entities.parking_space import ParkingSpace


class PostedParkingSpace(Entity):
    """
    Parking Space Entity with posting status

    """
    # required variables

    parking_space = ModelType(model_class=ParkingSpace, required=True)
    is_active = BooleanType(required=True, default=False)
    created_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
    updated_at = DateTimeType(required=True, serialized_format='%Y-%m-%d %H:%M:%S.%f')
